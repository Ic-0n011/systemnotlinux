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

base_path = Path(__file__).parent

MEDIA_PATH = base_path / "media"

BACKGROUND_PATH = MEDIA_PATH / "background.jpg"
BACKGROUND_MUSIC_PATH = MEDIA_PATH / "music.mp3"
CLICK_PATH = MEDIA_PATH / "click.wav"
