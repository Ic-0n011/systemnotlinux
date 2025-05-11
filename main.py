"""Модуль приложения."""

import pygame as pg

import config as cf
from quiz import Quiz


class App:
    """Приложение."""

    def __init__(self) -> None:
        """Приложение."""
        pg.init()
        self.screen = pg.display.set_mode(cf.SIZE_WINDOW)
        self.is_running = False
        self.scene = Quiz()
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
        self.scene.render(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    App()
