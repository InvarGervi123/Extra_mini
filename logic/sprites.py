"""
logic/sprites.py
כל אובייקט במשחק יורש מ-pygame.sprite.Sprite (דרישה).
Tank, Bullet, Wall, PowerUp.
"""

from __future__ import annotations
import pygame
from interfaces.controller import ITankController
from logic.settings import WIDTH, HEIGHT


class Tank(pygame.sprite.Sprite):
    """
    Tank:
    - זז לפי Controller (Interface)
    - יורה עם cooldown
    - hp
    """

    def __init__(self, tank_id: str, color: tuple[int, int, int], center: tuple[int, int], controller: ITankController):
        super().__init__()
        self.image = pygame.Surface((44, 32))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=center)

        self.tank_id = tank_id
        self.controller = controller

        self.hp = 5
        self.speed = 220.0

        self.dir_x, self.dir_y = (1, 0)  # כיוון ירי אחרון
        self.cooldown = 0.35
        self._cooldown_left = 0.0

    def update(self, dt: float) -> None:
        self._cooldown_left = max(0.0, self._cooldown_left - dt)

    def move_blocked_by_walls(self, dx: int, dy: int, dt: float, walls: pygame.sprite.Group) -> None:
        # עדכון כיוון ירי אחרון
        if dx != 0 or dy != 0:
            self.dir_x, self.dir_y = dx, dy

        # X
        old_x = self.rect.x
        self.rect.x += int(dx * self.speed * dt)
        self._clamp()
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x = old_x

        # Y
        old_y = self.rect.y
        self.rect.y += int(dy * self.speed * dt)
        self._clamp()
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y = old_y

    def _clamp(self) -> None:
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

    def try_shoot(self) -> "Bullet | None":
        if self._cooldown_left > 0:
            return None

        self._cooldown_left = self.cooldown

        bullet_speed = 520.0
        vx = self.dir_x * bullet_speed
        vy = self.dir_y * bullet_speed
        if vx == 0 and vy == 0:
            vx = bullet_speed

        return Bullet(self.rect.center, (vx, vy), self.tank_id)


class Bullet(pygame.sprite.Sprite):
    """קליע: זז ונמחק מחוץ למסך."""

    def __init__(self, center: tuple[int, int], vel: tuple[float, float], owner_id: str):
        super().__init__()
        self.image = pygame.Surface((10, 6))
        self.image.fill((255, 220, 80))
        self.rect = self.image.get_rect(center=center)

        self.vx, self.vy = vel
        self.owner_id = owner_id

    def update(self, dt: float) -> None:
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)

        if (
            self.rect.right < 0 or self.rect.left > WIDTH
            or self.rect.bottom < 0 or self.rect.top > HEIGHT
        ):
            self.kill()


class Wall(pygame.sprite.Sprite):
    """קיר סטטי."""

    def __init__(self, rect: pygame.Rect):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill((90, 90, 110))
        self.rect = rect.copy()


class PowerUp(pygame.sprite.Sprite):
    """
    PowerUp עם אנימציה של “פולס” (גדל/קטן).
    הפריימים מתקדמים דרך EVENT (ANIM_TICK_EVENT), לא דרך update.
    """

    def __init__(self, center: tuple[int, int]):
        super().__init__()
        self.frames = self._make_frames()
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)

    def _make_frames(self) -> list[pygame.Surface]:
        # 6 פריימים של ריבוע ירוק שגדל/קטן
        sizes = [16, 18, 20, 18, 16, 14]
        frames = []
        for s in sizes:
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            pygame.draw.rect(surf, (90, 255, 120, 255), pygame.Rect(0, 0, s, s), border_radius=4)
            frames.append(surf)
        return frames

    def next_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        center = self.rect.center
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)




class Explosion(pygame.sprite.Sprite):
    """
    Explosion אנימציה “פריימים”.
    לא משתמשים ב-update בשביל פריימים, אלא מקדמים פריים רק דרך EVENT.
    """

    def __init__(self, center: tuple[int, int]):
        super().__init__()
        self.frames: list[pygame.Surface] = self._make_frames()
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)

    def _make_frames(self) -> list[pygame.Surface]:
        # פריימים פשוטים: עיגול גדל (ממש קל להסביר בהגנה)
        sizes = [10, 16, 24, 32, 40]
        frames = []
        for s in sizes:
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 200, 60, 220), (s // 2, s // 2), s // 2)
            frames.append(surf)
        return frames

    def next_frame(self) -> None:
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.kill()
            return
        center = self.rect.center
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)
