# Импорт необходимых библиотек
import pygame  # Библиотека для создания графики, обработки событий и отрисовки
import pymunk  # Физический движок для расчёта движения, сил и столкновений
import pymunk.pygame_util  # Утилита для интеграции Pymunk с Pygame (упрощает отрисовку физических объектов)
import math  # Математические функции, например, для вычисления расстояний и нормализации векторов

# Инициализация Pygame
pygame.init()  # Запускает Pygame, подготавливая её для работы с графикой и событиями
width, height = 800, 600  # Размеры окна: 800 пикселей в ширину, 600 в высоту
screen = pygame.display.set_mode((width, height))  # Создаёт окно с заданными размерами
clock = pygame.time.Clock()  # Объект для контроля частоты кадров (FPS), чтобы симуляция работала плавно
font = pygame.font.SysFont("Arial", 20)  # Шрифт Arial размером 20 для отображения текста (скорости спутника)

# Инициализация Pymunk
space = pymunk.Space()  # Создаёт физическое пространство, где происходят все расчёты (движение, силы, столкновения)
space.gravity = (0, 0)  # Устанавливает гравитацию пространства равной нулю, так как мы сами моделируем гравитацию между объектами

# Класс Object — базовый класс для физических объектов (планеты и спутника)
class Object:
    def __init__(self, mass, size, position, velocity=(0, 0), color=(255, 255, 255, 255), static=False):
        # Конструктор класса, задаёт свойства объекта
        self.mass = mass  # Масса объекта (в кг), влияет на гравитационную силу
        self.size = size  # Радиус объекта (в пикселях), определяет его визуальный размер
        self.color = color  # Цвет в формате RGBA (красный, зелёный, синий, альфа), где альфа — прозрачность
        # Создаём физическое тело:
        # - mass: масса тела
        # - moment: момент инерции, рассчитанный для круга (pymunk.moment_for_circle)
        # - body_type: STATIC для неподвижных объектов (планета), DYNAMIC для подвижных (спутник)
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, size), body_type=pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC)
        self.body.position = position  # Начальная позиция тела (x, y) в пикселях
        self.body.velocity = velocity  # Начальная скорость (vx, vy) в пикселях/с
        self.shape = pymunk.Circle(self.body, size)  # Создаём форму — круг с заданным радиусом
        self.shape.color = color  # Задаём цвет формы для отрисовки
        self.shape.collision_type = 1 if static else 2  # Тип столкновения: 1 для планеты, 2 для спутника (для обработки столкновений)
        space.add(self.body, self.shape)  # Добавляем тело и форму в физическое пространство

    def update(self, objects):
        # Метод обновляет состояние объекта, рассчитывая гравитационные силы от других объектов
        for obj in objects:  # Перебираем все объекты в симуляции
            if obj != self:  # Не учитываем взаимодействие объекта с самим собой
                # Вычисляем расстояние между текущим объектом и другим
                distance = self.body.position.get_distance(obj.body.position)
                if distance < 500:  # Ограничиваем радиус действия гравитации до 500 пикселей
                    # Ограничиваем минимальное расстояние до 60 пикселей, чтобы избежать чрезмерной силы при сближении
                    effective_distance = max(distance, 60)
                    # Рассчитываем гравитационную силу
                    force = self.calculate_gravity(obj, effective_distance)
                    # Вычисляем направление силы (единичный вектор от текущего объекта к другому)
                    direction = (obj.body.position - self.body.position).normalized()
                    # Применяем силу к телу в точке его центра
                    self.body.apply_force_at_world_point(force * direction, self.body.position)

    def calculate_gravity(self, other, distance):
        # Рассчитывает гравитационную силу по закону Ньютона
        G = 100  # Гравитационная постоянная (увеличена для заметного эффекта в симуляции)
        # Формула: F = G * m1 * m2 / r^2
        return G * self.mass * other.mass / distance**2

# Подклассы Planet и Satellite
# Они наследуются от Object, но не добавляют новых методов, просто для удобства разделения
class Planet(Object):
    pass

class Satellite(Object):
    pass

# Обработчик столкновений
def collision_handler(arbiter, space, data):
    # Вызывается, когда спутник сталкивается с планетой
    satellite_shape = arbiter.shapes[1]  # Предполагаем, что второй объект — спутник
    satellite_shape.body.velocity = (0, 0)  # Останавливаем спутник при столкновении
    return False  # Запрещаем прохождение объектов друг через друга

# Создание объектов
planet = Planet(
    mass=1000,  # Масса планеты (1000 кг)
    size=50,  # Радиус планеты (50 пикселей)
    position=(400, 300),  # Позиция в центре экрана
    color=(0, 100, 255, 255),  # Синий цвет (RGBA)
    static=True  # Планета неподвижна
)
satellite = Satellite(
    mass=100,  # Масса спутника (100 кг)
    size=10,  # Радиус спутника (10 пикселей)
    position=(600, 300),  # Начальная позиция, расстояние до планеты r=200 пикселей
    velocity=(0, 22.36),  # Начальная скорость (первая космическая, рассчитана для круговой орбиты)
    color=(255, 255, 0, 255)  # Жёлтый цвет
)

objects = [planet, satellite]  # Список всех объектов для обновления

# Настройка обработчика столкновений
handler = space.add_collision_handler(1, 2)  # Указываем, что обрабатываем столкновения между типами 1 (планета) и 2 (спутник)
handler.begin = collision_handler  # Назначаем функцию обработки столкновений

# Список для хранения траектории спутника
trail = []  # Сохраняет до 100 последних позиций спутника для отрисовки пути

# Настройка отрисовки
draw_options = pymunk.pygame_util.DrawOptions(screen)  # Объект для отрисовки физических объектов Pymunk на экране Pygame

# Переопределяем метод draw_circle
def custom_draw_circle(pos, angle, radius, outline_color, fill_color):
    # Кастомная функция отрисовки круга, чтобы использовать возможности Pygame
    pygame.draw.circle(screen, fill_color, (int(pos.x), int(pos.y)), int(radius))

draw_options.draw_circle = custom_draw_circle  # Заменяем стандартный метод отрисовки кругов в Pymunk

# Основной цикл симуляции
running = True
while running:
    # Обработка событий (например, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            running = False  # Завершаем цикл

    # Обновление физики
    for obj in objects:  # Для каждого объекта
        obj.update(objects)  # Рассчитываем и применяем гравитационные силы
    space.step(1/120.0)  # Продвигаем физическую симуляцию на один шаг (1/120 секунды)

    # Сохранение траектории спутника
    trail.append(satellite.body.position)  # Добавляем текущую позицию спутника
    if len(trail) > 100:  # Ограничиваем длину траектории до 100 точек
        trail.pop(0)  # Удаляем старую точку

    # Отрисовка
    screen.fill((0, 0, 0))  # Заливаем экран чёрным цветом (очищаем)
    if len(trail) > 1:  # Если есть хотя бы 2 точки траектории
        # Рисуем серую линию, соединяющую точки траектории
        pygame.draw.lines(screen, (100, 100, 100), False, [(int(p.x), int(p.y)) for p in trail], 1)

    # Отображение скорости спутника
    speed = math.sqrt(satellite.body.velocity.x**2 + satellite.body.velocity.y**2)  # Вычисляем модуль скорости
    speed_text = font.render(f"Speed: {speed:.2f} pixels/s", True, (255, 255, 255))  # Создаём текст
    screen.blit(speed_text, (10, 10))  # Отображаем текст в верхнем левом углу

    space.debug_draw(draw_options)  # Отрисовываем физические объекты (планету и спутник)
    pygame.display.flip()  # Обновляем экран, показывая новый кадр
    clock.tick(120)  # Ограничиваем частоту до 120 FPS для плавной анимации

# Завершение работы
pygame.quit()  # Закрываем Pygame и освобождаем ресурсы