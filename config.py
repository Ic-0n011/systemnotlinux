"""Модуль конфигураций."""
from pathlib import Path

import pygame as pg

# Шрифты
pg.font.init()
FONT_BUTTON = pg.font.Font(None, 50)
FONT_QUESTIONBOX = pg.font.Font(None, 70)
FONT_TEXT = pg.font.Font(None, 70)

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BASE_PATH = Path(__file__).parent
