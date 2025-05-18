"""Модуль викторины."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import pygame as pg

import config as cfg


class Quiz:
    """Викторина."""

    def __init__(
            self,
            screen: pg.Surface,
            questions: list[dict],
            return_callback: Callable,
    ) -> None:
        """Викторина."""
        self.screen = screen
        self.questions = questions
        self.return_callback = return_callback

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

        self._create_text(text, (qubox_x, qubox_y), qubox_max_width)

        # Кнопки
        answer_idx = question["answer_idx"]
        options = question["options"]

        button_x = int(self.screen.get_width() * 0.16)
        button_y = int(self.screen.get_height() * 0.4)
        button_width = int(self.screen.get_width() * 0.60)
        button_margin = 20
        current_y = button_y

        for idx, option in enumerate(options):

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
                    # Показ статистики
                    self.sprites.empty()
                    text_y = int(self.screen.get_height() * 0.15)
                    text_x = int(self.screen.get_width() * 0.16)
                    text_max_width = int(self.screen.get_width() * 0.76)
                    percent = self.right_answer_counter / len(self.questions) * 100
                    text = f"Вы ответили правильно на {round(percent)}% вопросов. "
                    text += f"Дано правильных ответов - {self.right_answer_counter}, "
                    text += f"а неправильных - {self.wrong_answer_counter}. "
                    text += f"Всего вопросов {self.current_question_idx + 1}. "
                    self._create_text(text, (text_x, text_y), text_max_width)

                    button_x = int(self.screen.get_width() * 0.5)
                    button_y = int(self.screen.get_height() * 0.4)
                    button_width = int(self.screen.get_width() * 0.38)
                    option = "Вернуться в меню"
                    Button(
                        self.sprites,
                        self.wrap_text(option, cfg.FONT_BUTTON, button_width),
                        (button_x, button_y),
                        self.return_callback,
                        button_width,
                    )

            # Создание кнопки
            btn = Button(
                self.sprites,
                self.wrap_text(option, cfg.FONT_BUTTON, button_width),
                (button_x, current_y),
                lambda param=idx + 1: callback(param),
                max_width=button_width,
            )

            # Перемещение вниз для следующей кнопки
            current_y += btn.rect.height + button_margin

    def _create_text(
            self,
            text: str,
            coords: tuple[int, int],
            max_width: int,
    ) -> None:
        """Создает спрайты Text для каждой строки вопроса."""
        lines = self.wrap_text(text, cfg.FONT_TEXT, max_width)
        x, y = coords
        line_height = cfg.FONT_TEXT.get_height()
        for line in lines:
            Text(self.sprites, line, (x, y))
            y += line_height

    def wrap_text(self, text: str, font: pg.font.Font, max_width: int) -> list[str]:
        """Разбивает текст на строки, не превышающие max_width."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Проверяем, помещается ли слово целиком
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:  # noqa: PLR5501
                # Если слово слишком длинное, разбиваем его с дефисом
                if font.size(word)[0] > max_width:
                    temp_word = ""
                    for char in word:
                        test_word = temp_word + char + "-"
                        if font.size(current_line + test_word)[0] <= max_width:
                            temp_word += char
                        else:
                            # Добавляем текущую линию с дефисом
                            if current_line:
                                lines.append(current_line.strip())
                                current_line = ""
                            lines.append(temp_word + "-")
                            temp_word = char
                    # Оставшаяся часть слова
                    current_line = temp_word + " "
                else:
                    # Если слово помещается в новую строку
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "

        # Добавляем последнюю строку, если она не пустая
        if current_line:
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
    """Класс кнопки."""

    def __init__(
        self,
        group: pg.sprite.Group,
        option: list[str],
        coords: tuple[int, int],
        callback: Callable,
        max_width: int = 300,
        *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Кнопка."""
        super().__init__(*groups)
        group.add(self)
        self.option = option
        self.coords = coords
        self.callback = callback
        self.max_width = max_width
        self.font = cfg.FONT_BUTTON

        self.image = self._create_button_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords

    def _create_button_surface(self) -> pg.Surface:
        """Создаёт поверхность кнопки с фоном и текстом."""
        line_height = self.font.get_height()
        padding = 10
        box_height = line_height * len(self.option) + padding * 2
        surface = pg.Surface((self.max_width, box_height), pg.SRCALPHA)

        # Фон кнопки
        pg.draw.rect(surface, (230, 230, 230), surface.get_rect(), border_radius=6)

        # Рисуем текст
        for i, line in enumerate(self.option):
            text_surf = self.font.render(line, True, cfg.BLUE)
            surface.blit(text_surf, (padding, padding + i * line_height))

        return surface

    def on_click(self) -> None:
        """Действие на нажатие."""
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
        self.font = cfg.FONT_TEXT

        self.image = self.font.render(text, True, cfg.GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords


class Image(pg.sprite.Sprite):
    """Выводит изображение вместо текста."""

    def __init__(
            self,
            group: pg.sprite.Group,
            image_name: str,  # Имя файла изображения в папке media
            coords: tuple[int, int],
            *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Инициализирует спрайт с изображением из папки media."""
        super().__init__(*groups)
        group.add(self)
        self.coords = coords

        # Формируем путь к изображению в папке media
        media_path = Path("media") / image_name
        # Загружаем изображение
        self.image = pg.image.load(str(media_path)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords
