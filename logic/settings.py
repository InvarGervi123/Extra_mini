"""
logic/settings.py
הגדרות + שני אירועים מעוצבים (Custom Events).
"""

import pygame

WIDTH, HEIGHT = 900, 540
FPS = 60

BG = (18, 18, 24)

# Custom Events (נדרש לפחות 2)
POWERUP_EVENT = pygame.USEREVENT + 1   # spawn כוח
ROUND_TICK_EVENT = pygame.USEREVENT + 2  # טיימר של סיבוב

ANIM_TICK_EVENT = pygame.USEREVENT + 3  # טיק קבוע לאנימציות (פיצוצים/הבהובים)
