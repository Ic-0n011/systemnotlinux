"""Модуль викторины."""
from __future__ import annotations

from typing import Callable

import pygame as pg

import config as cf
from questions import easy


class Quiz:
    """Викторина."""

    def __init__(self, screen: pg.Surface) -> None:
        """Викторина."""
        self.screen = screen
        self.questions = easy
        self.current_question_idx = 0
        self.right_answer_counter = 0
        self.wrong_answer_counter = 0
        self.sprites = pg.sprite.Group()
        self.make_widjets()


    def make_widjets(self) -> None:
        """Создает спрайты для текущего вопроса."""
        question = self.questions[self.current_question_idx]

        # Счетчик
        counter = str(self.current_question_idx + 1) + " из " + str(len(self.questions))

        Text(self.sprites, counter, (10, 10))

        # Текст c вопросом
        text = question["text"]
        qubox_y = int(self.screen.get_height() * 0.15)
        qubox_x = int(self.screen.get_width() * 0.16)
        qubox_max_width = int(self.screen.get_width() * 0.8)

        self._create_question_text(text, (qubox_x, qubox_y), qubox_max_width)

        # Кнопки
        options = question["options"]
        answer_idx = question["answer_idx"]
        button_y = int(self.screen.get_height() * 0.75)
        button_x = int(self.screen.get_width() * 0.16)

        for num, option in enumerate(options, 1):
            def callback(num: int) -> None:
                """Эта функция вызывается при вызове кнопки."""
                if answer_idx == num - 1:
                    self.right_answer_counter += 1
                else:
                    self.wrong_answer_counter += 1

                if len(self.questions) > self.current_question_idx + 1:
                    self.current_question_idx += 1
                    self.sprites.empty()
                    self.make_widjets()
                else:
                    self.sprites.empty()
                    text_y = int(self.screen.get_height() * 0.15)
                    text_x = int(self.screen.get_width() * 0.16)
                    percent = self.right_answer_counter / len(self.questions) * 100
                    text = "Вы ответили правильно на " + str(percent) + "%"
                    Text(self.sprites, text, (text_x, text_y))
                print("Ты ответил правильно", self.right_answer_counter, "раз")
                print("и ответил не правильно", self.wrong_answer_counter, "раз")

            Button(
                self.sprites,
                option,
                (button_x * num, button_y),
                lambda param=num: callback(param),
            )

    def _create_question_text(
            self,
            text: str,
            coords: tuple[int, int],
            max_width: int,
    ) -> None:
        """Создает спрайты Text для каждой строки вопроса."""
        lines = self.wrap_text(text, cf.FONT_TEXT, max_width)
        x, y = coords
        line_height = cf.FONT_TEXT.get_height()
        for line in lines:
            Text(self.sprites, line, (x, y))
            y += line_height

    def wrap_text(self, text: str, font: pg.font.Font, max_width: int) -> list[str]:
        """Разбивает текст на строки, не превышающие max_width."""
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines

    def update(self) -> None:
        """Обновление событий."""

    def render(self) -> None:
        """Отрисовка."""
        self.sprites.draw(self.screen)

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
            *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Кнопочка."""
        super().__init__(*groups)
        group.add(self)
        self.text = text
        self.coords = coords
        self.callback = callback

        self.image = cf.FONT_BUTTON.render(text, True, cf.BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords

    def on_click(self) -> None | bool:
        """О нет на кнопку нажали, кто посмел."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.callback()


class Text(pg.sprite.Sprite):
    """Выводит данный ему текст."""

    def __init__(
            self,
            group: pg.sprite.Group,
            text: str,
            coords: tuple[int, int],
            *groups: pg.sprite.AbstractGroup,
            ) -> None:
        """Выводит данный ему текст."""
        super().__init__(*groups)
        group.add(self)
        self.text = text
        self.coords = coords
        self.font = cf.FONT_TEXT

        self.image = self.font.render(text, True, cf.GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords

