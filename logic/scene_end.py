"""
logic/scene_end.py
End Scene: GAME OVER + NEW GAME + MENU.
"""

import pygame
from interfaces.scene import IScene
from ui.button import Button
from logic.settings import WIDTH, HEIGHT, BG


class EndScene(IScene):
    def __init__(self, change_scene, message: str) -> None:
        self.change_scene = change_scene
        self.message = message

        self.font_title = pygame.font.SysFont(None, 64)
        self.font_btn = pygame.font.SysFont(None, 40)

        self.btn_again = Button(pygame.Rect(WIDTH // 2 - 160, 270, 320, 60), "NEW GAME", self.font_btn)
        self.btn_menu = Button(pygame.Rect(WIDTH // 2 - 160, 350, 320, 60), "MENU", self.font_btn)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.btn_again.clicked(event):
            self.change_scene("game")
        elif self.btn_menu.clicked(event):
            self.change_scene("menu")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_scene("menu")

    def update(self, dt: float) -> None:
        _ = dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG)

        title = self.font_title.render("GAME OVER", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))

        msg = self.font_title.render(self.message, True, (255, 220, 120))
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 220)))

        self.btn_again.draw(screen)
        self.btn_menu.draw(screen)
