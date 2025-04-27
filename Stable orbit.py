import pygame
import pymunk
import pymunk.pygame_util
import math

# Инициализация Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Инициализация Pymunk
space = pymunk.Space()
space.gravity = (0, 0)

# Класс Object
class Object:
    def __init__(self, mass, size, position, velocity=(0, 0), color=(255, 255, 255, 255), static=False):
        self.mass = mass
        self.size = size
        self.color = color
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, size), body_type=pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC)
        self.body.position = position
        self.body.velocity = velocity
        self.shape = pymunk.Circle(self.body, size)
        self.shape.color = color
        self.shape.collision_type = 1 if static else 2  # Для обработки столкновений
        space.add(self.body, self.shape)

    def update(self, objects):
        for obj in objects:
            if obj != self:
                distance = self.body.position.get_distance(obj.body.position)
                if distance < 500:
                    # Ограничиваем минимальное расстояние
                    effective_distance = max(distance, 60)
                    force = self.calculate_gravity(obj, effective_distance)
                    direction = (obj.body.position - self.body.position).normalized()
                    self.body.apply_force_at_world_point(force * direction, self.body.position)

    def calculate_gravity(self, other, distance):
        G = 100  # Уменьшенная гравитационная постоянная
        return G * self.mass * other.mass / distance**2

# Подклассы
class Planet(Object):
    pass

class Satellite(Object):
    pass

# Обработчик столкновений
def collision_handler(arbiter, space, data):
    # При столкновении спутника с планетой останавливаем спутник
    satellite_shape = arbiter.shapes[1]
    satellite_shape.body.velocity = (0, 0)
    return False  # Запрещаем прохождение сквозь планету

# Создание объектов
planet = Planet(
    mass=1000,
    size=50,
    position=(400, 300),
    color=(0, 100, 255, 255),
    static=True
)
satellite = Satellite(
    mass=100,
    size=10,
    position=(600, 300),  # Новое расстояние r=200
    velocity=(0, 22.36),  # Первая космическая скорость
    color=(255, 255, 0, 255)
)

objects = [planet, satellite]

# Настройка обработчика столкновений
handler = space.add_collision_handler(1, 2)  # 1 - планета, 2 - спутник
handler.begin = collision_handler

# Список для траектории
trail = []

# Настройка отрисовки
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Переопределяем draw_circle
def custom_draw_circle(pos, angle, radius, outline_color, fill_color):
    pygame.draw.circle(screen, fill_color, (int(pos.x), int(pos.y)), int(radius))

draw_options.draw_circle = custom_draw_circle

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление физики
    for obj in objects:
        obj.update(objects)
    space.step(1/120.0)  # Уменьшенный шаг для стабильности

    # Сохранение траектории
    trail.append(satellite.body.position)
    if len(trail) > 100:
        trail.pop(0)

    # Отрисовка
    screen.fill((0, 0, 0))
    if len(trail) > 1:
        pygame.draw.lines(screen, (100, 100, 100), False, [(int(p.x), int(p.y)) for p in trail], 1)

    # Отображение скорости
    speed = math.sqrt(satellite.body.velocity.x**2 + satellite.body.velocity.y**2)
    speed_text = font.render(f"Speed: {speed:.2f} pixels/s", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))

    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()