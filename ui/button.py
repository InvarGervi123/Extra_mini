"""
ui/button.py
כפתור UI פשוט: ציור + בדיקת קליק.
"""

import pygame


class Button:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font) -> None:
        self.rect = rect
        self.text = text
        self.font = font

    def clicked(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        return self.rect.collidepoint(event.pos)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (45, 45, 55), self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=10)

        surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=self.rect.center))
