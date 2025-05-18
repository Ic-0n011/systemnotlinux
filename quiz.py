"""Модуль викторины."""
from __future__ import annotations

from typing import Callable

import pygame as pg

import config as cfg


class Quiz:
    """Викторина."""

    def __init__(
            self,
            screen: pg.Surface,
            questions: list[dict],
            return_callback: Callable[[], None],
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
        text_x = int(self.screen.get_width() * 0.07)
        text_y = int(self.screen.get_height() * 0.15)
        text_max_width = int(self.screen.get_width() * 0.68)
        self._create_text(question["text"], (text_x, text_y), text_max_width)

        # Изображение (если есть, справа от текста)
        image_x = int(self.screen.get_width() * 0.79)
        image_y = int(self.screen.get_height() * 0.15)
        image_max_size = int(self.screen.get_height() * 0.27)
        image_name = question.get("image_name")
        if image_name:
            Image(self.sprites, image_name, (image_x, image_y), image_max_size)

        # Кнопки
        button_x = int(self.screen.get_width() * 0.2)
        button_y = int(self.screen.get_height() * 0.6)
        button_width = int(self.screen.get_width() * 0.6)
        button_margin = 20
        current_y = button_y

        answer_idx = question["answer_idx"]
        options = question["options"]

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

                    # Кнопка "Вернуться в меню"
                    button_x = int(self.screen.get_width() * 0.6)
                    button_y = int(self.screen.get_height() * 0.8)
                    button_width = int(self.screen.get_width() * 0.38)
                    option = "Вернуться в меню"
                    Button(
                        self.sprites,
                        self.wrap_text(option, cfg.FONT_BUTTON, button_width),
                        (button_x, button_y),
                        self.return_callback,
                        max_width=button_width,
                    )

            # Создание кнопки
            btn = Button(
                self.sprites,
                self.wrap_text(option, cfg.FONT_BUTTON, button_width),
                (button_x, current_y),
                lambda param=idx + 1: callback(param),
                max_width=button_width,
            )
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
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            elif font.size(word)[0] > max_width:
                temp_word = ""
                for char in word:
                    test_word = temp_word + char + "-"
                    if font.size(current_line + test_word)[0] <= max_width:
                        temp_word += char
                    else:
                        if current_line:
                            lines.append(current_line.strip())
                            current_line = ""
                        lines.append(temp_word + "-")
                        temp_word = char
                current_line = temp_word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
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
        pg.mixer.init()
        self.click = pg.mixer.Sound(cfg.CLICK_PATH)

    def _create_button_surface(self) -> pg.Surface:
        """Создаёт поверхность кнопки с фоном и текстом."""
        line_height = self.font.get_height()
        padding = 10
        box_height = line_height * len(self.option) + padding * 2
        surface = pg.Surface((self.max_width, box_height), pg.SRCALPHA)
        pg.draw.rect(surface, (230, 230, 230), surface.get_rect(), border_radius=6)
        for i, line in enumerate(self.option):
            text_surf = self.font.render(line, True, cfg.BLUE)
            surface.blit(text_surf, (padding, padding + i * line_height))
        return surface

    def on_click(self) -> None:
        """Действие на нажатие."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.click.play()
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
    """Выводит изображение."""

    def __init__(
            self,
            group: pg.sprite.Group,
            image_name: str,
            coords: tuple[int, int],
            image_max_size: int,
            *groups: pg.sprite.AbstractGroup,
    ) -> None:
        """Инициализирует спрайт с изображением из папки media."""
        super().__init__(*groups)
        group.add(self)
        self.coords = coords
        self.image_max_size = image_max_size
        image_path = cfg.MEDIA_PATH / image_name
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (image_max_size, image_max_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords
