"""Модуль викторины."""

from typing import Callable
import pygame as pg

import config as cf
from questions import easy


class Quiz:
    """Викторина."""

    def __init__(self) -> None:
        """Викторина."""
        self.questions = easy
        self.current_question_idx = 0
        self.right_answer_counter = 0
        self.wrong_answer_counter = 0
        self.sprites = pg.sprite.Group()
        self.make_widjets()

    def make_widjets(self) -> None:
        """Создает спрайты для текущего вопроса."""
        question = self.questions[self.current_question_idx]
        text = question["text"]
        options = question["options"]
        answer_idx = question["answer_idx"]

        button_y = 500 #FIXME: расичтать от размера экрана

        for num, option in enumerate(options, 1):

            def callback(num) -> None:
                """Эта функция вызывается при вызове кнопки."""
                print("Нажата кнопка ", num)
                if answer_idx == num - 1:
                    self.right_answer_counter += 1
                else:
                    self.wrong_answer_counter += 1

                print(self.right_answer_counter, self.wrong_answer_counter)

            Button(self.sprites, option, (100 * num, button_y), lambda param=num: callback(param))

    def update(self) -> None:
        """Обновление событий."""

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка."""
        font = pg.font.Font(None, 70)
        surface = font.render(self.questions[0]["text"], True, (255, 255, 255))  # noqa: FBT003
        screen.blit(surface, (100, 100))

        self.sprites.draw(screen)

    def handle_events(self, events: list[pg.event.Event]) -> None:
        """Реакция на события."""
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in self.sprites:
                    if isinstance(sprite, Button):
                        sprite.on_click()





class Button(pg.sprite.Sprite):
    """Кнопка."""

    def __init__(
            self,
            group: pg.sprite.Group,
            text: str,
            coords: tuple[int, int],
            callback: Callable,
    ) -> None:
        """Кнопочка."""
        super().__init__()
        self.text = text
        self.callback = callback
        font = pg.font.Font(None, 50)
        self.image = font.render(text, True, (0, 255, 0), (255, 0, 0))  # noqa: FBT003
        self.coords = coords
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords
        group.add(self)

    def on_click(self) -> None | bool:
        """О нет на кнопку нажали, кто посмел."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.callback()
