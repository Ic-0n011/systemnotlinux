"""Модуль викторины."""

import pygame as pg

import config as cf
from questions import easy


class Quiz:
    """Викторина."""

    def __init__(self) -> None:
        """Викторина."""
        self.questions = easy
        self.current_question_idx = 0
        self.buttons = []
        self.load_quesion()

    def load_quesion(self) -> None:
        """Загрузка вопроса."""
        position = 0
        for i in self.questions[self.current_question_idx]["options"]:
            position += cf.SIZE_WINDOW[0] / 5
            self.buttons.append(Button(i, (position, 500)))


    def update(self) -> None:
        """Обновление событий."""

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка."""
        font = pg.font.Font(None, 70)
        surface = font.render(self.questions[0]["text"], True, (255, 255, 255))  # noqa: FBT003
        screen.blit(surface, (100, 100))

        for button in self.buttons:
            button.render(screen)

    def handle_events(self, events: list[pg.event.Event]) -> None:
        """Реакция на события."""
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    button.on_click()


class Button:
    """Кнопка."""

    def __init__(self, text: str, coords: tuple[int, int]) -> None:
        """Кнопочка."""
        self.text = text
        font = pg.font.Font(None, 50)
        self.surface = font.render(text, True, (0, 255, 0), (255, 0, 0))  # noqa: FBT003
        self.coords = coords
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.coords

    def render(self, screen: pg.Surface) -> None:
        """Рисуем кнопочку."""
        screen.blit(self.surface, self.coords)

    def on_click(self) -> None:
        """О нет на кнопку нажали, кто посмел."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            print(True)  # noqa: FBT003, T201
