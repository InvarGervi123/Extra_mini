"""
logic/scene_menu.py
Menu Scene: START / QUIT.
"""

import pygame
from interfaces.scene import IScene
from ui.button import Button
from logic.settings import WIDTH, HEIGHT, BG


class MenuScene(IScene):
    def __init__(self, change_scene) -> None:
        self.change_scene = change_scene
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_btn = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 26)

        self.btn_start = Button(pygame.Rect(WIDTH // 2 - 140, 230, 280, 60), "START", self.font_btn)
        self.btn_quit = Button(pygame.Rect(WIDTH // 2 - 140, 310, 280, 60), "QUIT", self.font_btn)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.btn_start.clicked(event):
            self.change_scene("game")
        elif self.btn_quit.clicked(event):
            self.change_scene("quit")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_scene("quit")

    def update(self, dt: float) -> None:
        _ = dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG)

        title = self.font_title.render("TANK DUEL", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

        self.btn_start.draw(screen)
        self.btn_quit.draw(screen)

        hint = self.font_small.render("P1: WASD+SPACE | P2: Arrows+CTRL | ESC: Menu", True, (220, 220, 220))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 30)))
