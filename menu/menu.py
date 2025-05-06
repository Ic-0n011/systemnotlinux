"""модуль меню."""

import pygame
from menu_config import (
    BLACK,
    BUTTON_COLOR,
    FPS,
    WHITE,
)

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("123")

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

font = pygame.font.SysFont("Arial", 40)


class Button:
    """Класс для кнопки, отображаемой на экране."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
    ) -> None:
        """Инициализация кнопки."""
        x, y = position
        width, height = size
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x // 2, y // 2)
        self.text = text

    def draw(self, screen: pygame.Surface) -> None:
        """Отображает кнопку на экране."""
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2,
            ),
        )

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        """Проверяет, была ли нажата кнопка по переданным координатам."""
        return self.rect.collidepoint(pos)


class MainMenu:
    """Класс для главного меню игры."""

    def __init__(self) -> None:
        """Инициализация главного меню и кнопок."""
        self.running = True
        self.start_button = Button(
            position=(screen.get_width(), screen.get_height() - 100),
            size=(200, 50),
            text="Start Game",
        )
        self.quit_button = Button(
            position=(screen.get_width(), screen.get_height() + 100),
            size=(200, 50),
            text="Quit",
        )
        # self.mainloop()

    def mainloop(self) -> None:
        """Главный цикл."""
        while self.running:
            self.handle_events()
            self.draw()
            self.update()
            pygame.time.Clock().tick(FPS)
        pygame.quit()

    def handle_events(self) -> None:
        """Обработка событий (например, нажатия на кнопки)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(event.pos):
                    print("1")
                if self.quit_button.is_clicked(event.pos):
                    print("2")
                    self.running = False

    def draw(self) -> None:
        """Отображение кнопок и фона на экране."""
        screen.fill(WHITE)
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

    def update(self) -> None:
        """Обновление экрана."""
        pygame.display.flip()


if __name__ == "__main__":
    menu = MainMenu()
    menu.mainloop()
