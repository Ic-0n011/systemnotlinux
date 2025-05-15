"""Модуль викторины."""
from __future__ import annotations

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


    def make_widjets(self, screen: pg.Surface) -> None:
        """Создает спрайты для текущего вопроса."""
        question = self.questions[self.current_question_idx]
        text = question["text"]
        options = question["options"]
        answer_idx = question["answer_idx"]

        qubox_y = int(screen.get_height() * 0.15)
        qubox_x = int(screen.get_width() * 0.16)
        qubox_max_width = int(screen.get_width() * 0.8)

        QuestionBox(self.sprites, text, (qubox_x, qubox_y), qubox_max_width)

        button_y = int(screen.get_height() * 0.75)
        button_x = int(screen.get_width() * 0.16)

        for num, option in enumerate(options, 1):
            def callback(num: int) -> None:
                """Эта функция вызывается при вызове кнопки."""
                if answer_idx == num - 1:
                    self.right_answer_counter += 1
                else:
                    self.wrong_answer_counter += 1

            Button(
                self.sprites,
                option,
                (button_x * num, button_y),
                lambda param=num: callback(param),
            )

    def update(self) -> None:
        """Обновление событий."""

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка."""
        self.make_widjets(screen)
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
            *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Кнопочка."""
        super().__init__(*groups)
        group.add(self)
        self.text = text
        self.coords = coords
        self.callback = callback

        self.image = cf.FONT_BUTTON.render(text, True, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords

    def on_click(self) -> None | bool:
        """О нет на кнопку нажали, кто посмел."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.callback()


class QuestionBox(pg.sprite.Sprite):
    """Спрайт с вопросом."""

    def __init__(
            self,
            group: pg.sprite.Group,
            text: str,
            coords: tuple[int, int],
            max_width: int,
            *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Спрайт с вопросом."""
        super().__init__(*groups)
        group.add(self)
        self.text = text
        self.coords = coords
        self.max_width = max_width
        self.font = cf.FONT_QUESTIONBOX

        # Создаем изображение и прямоугольник
        self.image, self.rect = self._render_text()
        self.rect.topleft = self.coords

    def _render_text(self) -> tuple[pg.Surface, pg.Rect]:
        """Рендерит текст с переносом на строки."""
        # Разбиваем текст на строки
        words = self.text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        # Создаем поверхность для всех строк
        line_height = self.font.get_height()
        total_height = len(lines) * line_height
        image = pg.Surface((self.max_width, total_height), pg.SRCALPHA)

        # Рендерим строки
        for i, line in enumerate(lines):
            rendered_text = self.font.render(line, True, cf.RED)
            image.blit(rendered_text, (0, i * line_height))

        rect = image.get_rect()
        return image, rect
