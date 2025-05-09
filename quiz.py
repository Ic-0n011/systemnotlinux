"""Модуль викторины."""

import pygame as pg

from questions import easy


class Quiz:
    """Викторина."""

    def __init__(self) -> None:
        """Викторина."""
        self.questions = easy
        self.current_question_idx = 0
        self.buttons = [Button("123", (300, 300))]
        # TODO @Ic0n: 4 кнопки каждая берет текст  под своим номером. https://vscode.dev/github/Ic-0n011/systemnotlinux/blob/main/quiz.py#L15

    def load_quesion(self) -> None:
        """Загрузка вопроса."""


    def update(self) -> None:
        """Обновление событий."""

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка."""
        font = pg.font.Font(None, 30)
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
        font = pg.font.Font(None, 30)
        self.surface = font.render(text, True, (0, 0, 255), (255, 0, 0))  # noqa: FBT003
        self.coords = coords
        self.rect = self.surface.get_rect()
        self.rect.center = self.coords

    def render(self, screen: pg.Surface) -> None:
        """Рисуем кнопочку."""
        screen.blit(self.surface, self.coords)

    def on_click(self) -> None:
        """О нет на кнопку нажали, кто посмел."""  # noqa: RUF002 <- немного подташнивает
        if self.rect.collidepoint(pg.mouse.get_pos()):
            # TODO @Ic0n: сравнять видимое и невидимое (рект и поверхность  смещенны) https://vscode.dev/github/Ic-0n011/systemnotlinux/blob/main/quiz.py#L42-L62
            print(True)  # noqa: FBT003, T201
