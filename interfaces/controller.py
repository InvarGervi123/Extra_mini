"""
interfaces/controller.py
Interface לקלט של טנק.
Polymorphism: Tank לא יודע אם זה שחקן 1 או 2 - הוא רק שואל Controller.
"""

from abc import ABC, abstractmethod
import pygame


class ITankController(ABC):
    @abstractmethod
    def move(self, keys: pygame.key.ScancodeWrapper) -> tuple[int, int]:
        """מחזיר dx, dy (כל אחד -1/0/1)."""
        raise NotImplementedError

    @abstractmethod
    def shoot(self, keys: pygame.key.ScancodeWrapper) -> bool:
        """האם רוצים לירות עכשיו."""
        raise NotImplementedError


class P1Controller(ITankController):
    """שחקן 1: WASD + SPACE"""

    def move(self, keys: pygame.key.ScancodeWrapper) -> tuple[int, int]:
        dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        return dx, dy

    def shoot(self, keys: pygame.key.ScancodeWrapper) -> bool:
        return bool(keys[pygame.K_SPACE])


class P2Controller(ITankController):
    """שחקן 2: חצים + CTRL"""

    def move(self, keys: pygame.key.ScancodeWrapper) -> tuple[int, int]:
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        return dx, dy

    def shoot(self, keys: pygame.key.ScancodeWrapper) -> bool:
        return bool(keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])
