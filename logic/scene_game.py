"""
logic/scene_game.py
Game Scene:
- 2 טנקים
- ירי + פגיעות
- קירות
- PowerUp שמוסיף חיים
- 2 Custom Events:
  POWERUP_EVENT (spawn כל 6 שניות)
  ROUND_TICK_EVENT (כל שנייה מוריד זמן)
- ESC חוזר ל-Menu בכל זמן
"""

from __future__ import annotations
import random
import pygame

from interfaces.scene import IScene
from interfaces.controller import P1Controller, P2Controller
from logic.settings import WIDTH, HEIGHT, BG, POWERUP_EVENT, ROUND_TICK_EVENT, ANIM_TICK_EVENT
from logic.sprites import Tank, Bullet, Wall, PowerUp, Explosion


class GameScene(IScene):
    def __init__(self, change_scene) -> None:
        self.change_scene = change_scene
        self.font = pygame.font.SysFont(None, 28)

        # Groups (סדר פשוט):
        self.walls = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all = pygame.sprite.Group()

        self.explosions = pygame.sprite.Group()


        self._build_walls()

        self.p1 = Tank("p1", (70, 170, 255), (140, HEIGHT // 2), P1Controller())
        self.p2 = Tank("p2", (255, 110, 110), (WIDTH - 140, HEIGHT // 2), P2Controller())
        self._add(self.p1, self.tanks)
        self._add(self.p2, self.tanks)

        self.time_left = 60

        # Custom event timers
        pygame.time.set_timer(POWERUP_EVENT, 6000)
        pygame.time.set_timer(ROUND_TICK_EVENT, 1000)

        pygame.time.set_timer(ANIM_TICK_EVENT, 120)  # כל 120ms מקדמים פריימים באנימציות


    def _add(self, sprite: pygame.sprite.Sprite, group: pygame.sprite.Group) -> None:
        self.all.add(sprite)
        group.add(sprite)

    def _build_walls(self) -> None:
        rects = [
            pygame.Rect(WIDTH // 2 - 25, 120, 50, 140),
            pygame.Rect(WIDTH // 2 - 25, HEIGHT - 260, 50, 140),
            pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 - 18, 120, 36),
            pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 - 18, 120, 36),
        ]
        for r in rects:
            w = Wall(r)
            self._add(w, self.walls)

    def handle_event(self, event: pygame.event.Event) -> None:
        # ניווט בכל זמן
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._stop_timers()
            self.change_scene("menu")
            return

        # Custom Event #1
        if event.type == POWERUP_EVENT:
            self._spawn_powerup()

        # Custom Event #2
        if event.type == ROUND_TICK_EVENT:
            self.time_left -= 1
            if self.time_left <= 0:
                self._finish_by_time()

        if event.type == ANIM_TICK_EVENT:
        # מקדם פריימים של PowerUps
            for pu in self.powerups:
                pu.next_frame()

            # מקדם פריימים של פיצוצים
            for ex in self.explosions:
                ex.next_frame()


    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        self._update_tank(self.p1, keys, dt)
        self._update_tank(self.p2, keys, dt)

        self.all.update(dt)

        # bullets vs walls
        pygame.sprite.groupcollide(self.bullets, self.walls, True, False)

        # bullets vs tanks
        self._handle_hits()

        # tank vs powerup
        self._handle_powerups()

        # סיום אם hp נגמר
        if self.p1.hp <= 0:
            self._finish("Player 2 Wins!")
        elif self.p2.hp <= 0:
            self._finish("Player 1 Wins!")

    def _update_tank(self, tank: Tank, keys, dt: float) -> None:
        dx, dy = tank.controller.move(keys)
        tank.move_blocked_by_walls(dx, dy, dt, self.walls)

        if tank.controller.shoot(keys):
            b = tank.try_shoot()
            if b is not None:
                self._add(b, self.bullets)

    def _handle_hits(self) -> None:
        for b in list(self.bullets):
            hit = pygame.sprite.spritecollideany(b, self.tanks)
            if hit is None:
                continue

            # לא פוגעים בבעלים
            if isinstance(hit, Tank) and hit.tank_id == b.owner_id:
                continue

            b.kill()
            if isinstance(hit, Tank):
                hit.hp -= 1
                ex = Explosion(hit.rect.center)
                self._add(ex, self.explosions)


    def _handle_powerups(self) -> None:
        for tank in (self.p1, self.p2):
            pu = pygame.sprite.spritecollideany(tank, self.powerups)
            if pu:
                pu.kill()
                tank.hp = min(8, tank.hp + 2)

    def _spawn_powerup(self) -> None:
        for _ in range(40):
            x = random.randint(80, WIDTH - 80)
            y = random.randint(80, HEIGHT - 80)
            pu = PowerUp((x, y))

            if pygame.sprite.spritecollideany(pu, self.walls):
                continue
            if pygame.sprite.spritecollideany(pu, self.tanks):
                continue

            self._add(pu, self.powerups)
            return

    def _finish_by_time(self) -> None:
        if self.p1.hp > self.p2.hp:
            self._finish("Time! Player 1 Wins!")
        elif self.p2.hp > self.p1.hp:
            self._finish("Time! Player 2 Wins!")
        else:
            self._finish("Time! Draw!")

    def _finish(self, message: str) -> None:
        self._stop_timers()

        pygame.time.set_timer(ANIM_TICK_EVENT, 0)

        self.change_scene("end", message)

    def _stop_timers(self) -> None:
        pygame.time.set_timer(POWERUP_EVENT, 0)
        pygame.time.set_timer(ROUND_TICK_EVENT, 0)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG)
        self.all.draw(screen)

        hud = f"P1 HP:{self.p1.hp}   P2 HP:{self.p2.hp}   Time:{self.time_left}s"
        surf = self.font.render(hud, True, (255, 255, 255))
        screen.blit(surf, (16, 12))

        hint = self.font.render("ESC: Menu", True, (220, 220, 220))
        screen.blit(hint, (16, HEIGHT - 28))
