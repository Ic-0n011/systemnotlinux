"""Модуль приложения."""

from pathlib import Path
from typing import Callable

import pygame as pg

import config as cfg
from questions import easy, hard, medium
from quiz import Button, Quiz, Text


class App:
    """Приложение."""

    def __init__(self) -> None:
        """Приложение."""
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode()
        self.is_running = False

        # Загрузка фона

        background_path = cfg.BASE_PATH / "media" / "background.jpg"
        background_music_path = cfg.BASE_PATH / "media" / "music.mp3"

        self.background = pg.image.load(str(background_path)).convert()
        pg.mixer.music.load(background_music_path)

        screen_size = self.screen.get_size()
        img_rect = self.background.get_rect()
        crop_rect = pg.Rect(
            (img_rect.width - screen_size[0]) // 2,
            (img_rect.height - screen_size[1]) // 2,
            screen_size[0],
            screen_size[1],
        )
        self.background = self.background.subsurface(crop_rect)

        # Словарь сложностей
        self.difficulty_questions = {
            "Лаборант космической программы": easy,
            "Нобелевский лауреат": medium,
            "Автор теории Всего": hard,
        }

        # Передаем ключи словаря в Menu
        self.scene = Menu(
            self.screen,
            self.start_quiz,
            list(self.difficulty_questions.keys()),
        )

        self.mainloop()

    def start_quiz(self, difficulty: str) -> None:
        """Запускает викторину с выбранной сложностью."""
        questions = self.difficulty_questions[difficulty]
        self.scene = Quiz(self.screen, questions, self.return_to_menu)

    def return_to_menu(self) -> None:
        """Возвращает в меню."""
        self.scene = Menu(
            self.screen,
            self.start_quiz,
            list(self.difficulty_questions.keys()),
        )

    def mainloop(self) -> None:
        """Главный цикл."""
        self.is_running = True
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops=-1)
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.mixer.music.stop()
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

        self.scene.handle_events(events)

    def render(self) -> None:
        """Отрисовка."""
        self.screen.blit(self.background, (0, 0))
        self.scene.render()
        pg.display.flip()


class Menu:
    """Меню."""

    def __init__(
        self,
        screen: pg.Surface,
        callback: Callable[[str], None],
        difficulties: list[str],  # Новый параметр для списка ключей
    ) -> None:
        """Меню выбора сложности."""
        self.screen = screen
        self.callback = callback
        self.difficulties = difficulties  # Сохраняем переданные ключи
        self.sprites = pg.sprite.Group()
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Создает элементы меню."""
        screen_width, screen_height = self.screen.get_size()

        # Заголовок
        title_text = "Выберите сложность"
        title_surf = cfg.FONT_TEXT.render(title_text, True, cfg.GREEN)
        title_x = (screen_width - title_surf.get_width()) / 2
        title_y = int(screen_height * 0.1)
        Text(self.sprites, title_text, (title_x, title_y))

        # Кнопки
        button_width = int(screen_width * 0.4)
        button_x = (screen_width - button_width) / 2
        button_y_start = int(screen_height * 0.4)
        button_margin = 20
        current_y = button_y_start

        for diff in self.difficulties:
            button_text = [diff]
            btn = Button(
                self.sprites,
                button_text,
                (button_x, current_y),
                lambda d=diff: self.callback(d),  # Передаем ключ напрямую
                max_width=button_width,
            )
            current_y += btn.rect.height + button_margin

    def update(self) -> None:
        """Обновление."""

    def render(self) -> None:
        """Отрисовка меню."""
        self.sprites.draw(self.screen)

    def handle_events(self, events: list[pg.event.Event]) -> None:
        """Обработка событий."""
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in self.sprites:
                    if isinstance(sprite, Button):
                        sprite.on_click()


if __name__ == "__main__":
    App()

"""
TODO:
    картинки к вопросам
    таймер
"""
