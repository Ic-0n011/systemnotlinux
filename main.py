"""Модуль приложения."""

from pathlib import Path

import pygame as pg

import config as cf
from quiz import Quiz


class App:
    """Приложение."""

    def __init__(self) -> None:
        """Приложение."""
        pg.init()
        # Полноэкранный режим
        self.screen = pg.display.set_mode()
        self.is_running = False
        self.scene = Quiz(self.screen)

        # Формируем абсолютный путь к файлу
        base_path = Path(__file__).parent
        background_path = base_path / "media" / "background.jpg"

        self.background = pg.image.load(str(background_path)).convert()

        # Обрезаем изображение под размер экрана
        screen_size = self.screen.get_size()
        img_rect = self.background.get_rect()
        # Центрируем и обрезаем, чтобы соответствовать экрану
        crop_rect = pg.Rect(
            (img_rect.width - screen_size[0]) // 2,
            (img_rect.height - screen_size[1]) // 2,
            screen_size[0],
            screen_size[1],
        )
        self.background = self.background.subsurface(crop_rect)

        self.mainloop()

    def mainloop(self) -> None:
        """Главный цикл."""
        self.is_running = True
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()

    def update(self) -> None:
        """Обновление событий."""
        self.scene.update()

    def handle_events(self) -> None:
        """Сбор событий и реакция на них."""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
                else:
                    pass
        self.scene.handle_events(events)

    def render(self) -> None:
        """Отрисовка."""
        # Отрисовываем фоновое изображение вместо заливки цветом
        self.screen.blit(self.background, (0, 0))
        self.scene.render()
        pg.display.flip()


if __name__ == "__main__":
    App()


"""
TODO:
    картинки к вопросам
    таймер
    дать выбор уровня сложности
    рестарт
    больше вопросов
    музыка
    фон в виде космоса
"""
