"""
interfaces/scene.py
Interface (Abstraction) לסצנות: Menu / Game / End.
"""

from abc import ABC, abstractmethod
import pygame


class IScene(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """טיפול באירועים (מקלדת/עכבר/Custom)."""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        """עדכון לוגיקה לפי dt בשניות."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """ציור למסך."""
        raise NotImplementedError
