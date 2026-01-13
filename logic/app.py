"""
logic/app.py
מנהל חלון + לולאה + החלפת סצנות.
Polymorphism: app עובד מול IScene בלבד.
"""

from __future__ import annotations
import pygame

from interfaces.scene import IScene
from logic.settings import WIDTH, HEIGHT, FPS
from logic.scene_menu import MenuScene
from logic.scene_game import GameScene
from logic.scene_end import EndScene


class App:
    def __init__(self) -> None:
        pygame.init()
        
        # ---------- MUSIC (background) ----------
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/background.mp3")
        pygame.mixer.music.set_volume(0.3)  # 0.0 - 1.0
        pygame.mixer.music.play(-1)         # -1 = loop forever
        # ---------------------------------------

        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tank Duel (Simple)")

        self.clock = pygame.time.Clock()
        self.running = True

        self.scene: IScene = MenuScene(self._change_scene)

    def _change_scene(self, name: str, data: str | None = None) -> None:
        if name == "quit":
            self.running = False
            return

        if name == "menu":
            self.scene = MenuScene(self._change_scene)
            return

        if name == "game":
            self.scene = GameScene(self._change_scene)
            return

        if name == "end":
            msg = data if data is not None else "Game Over"
            self.scene = EndScene(self._change_scene, msg)
            return

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
