import pytest
import pygame
from pygame.locals import *

# Импортируйте классы Player и Environment и bubble_sort из вашего модуля
from main import Player, Environment, bubble_sort

"""
    Тест сортировки базы данных
"""
# Positive test cases
def test_bubble_sort_positive():
    # Создаем список данных для сортировки
    data = [('Result', '2024-05-29 21:31:08.858149', 18),
            ('Result', '2024-05-29 21:31:55.009608', 15),
            ('Result', '2024-05-29 21:33:08.846203', 5),
            ('Result', '2024-05-29 21:34:25.103373', 18),
            ('Result', '2024-05-29 21:35:10.472828', 16),
            ('Result', '2024-05-29 21:35:23.823227', 1)]
    
    # Ожидаемый результат после сортировки
    expected_result = [('Result', '2024-05-29 21:31:08.858149', 18),
                       ('Result', '2024-05-29 21:34:25.103373', 18),
                       ('Result', '2024-05-29 21:35:10.472828', 16),
                       ('Result', '2024-05-29 21:31:55.009608', 15),
                       ('Result', '2024-05-29 21:33:08.846203', 5),
                       ('Result', '2024-05-29 21:35:23.823227', 1)]
    
    # Вызываем функцию сортировки
    bubble_sort(data)
    
    # Проверяем, что результат совпадает с ожидаемым
    assert data == expected_result

def test_bubble_sort_invalid_data():
    # Создаем список данных с некорректными элементами
    data = [('Result', '2024-05-29 21:31:08.858149', 18),
            ('Result', '2024-05-29 21:31:55.009608', 15),
            ('Result', '2024-05-29 21:33:08.846203', 5),
            ('Result', '2024-05-29 21:34:25.103373'),
            ('Result', '2024-05-29 21:35:10.472828', 16),
            ('Result', '2024-05-29 21:35:23.823227', 1)]
    
    # Проверяем, что функция вызывает исключение IndexError
    with pytest.raises(IndexError):
        bubble_sort(data)

"""
    Тест обработки коллизии с картой
"""
# Игровые переменные
SQUARE_SIZE = 20
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
# Инициализация Pygame
pygame.init()

# Создание фиктивного экрана, который нужен для работы Pygame
screen = pygame.display.set_mode((800, 600))

@pytest.fixture
def environment():
    # Создание тестовой карты данных
    data = [
        [1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    return Environment(data)

@pytest.fixture
def player():
    # Создание игрока с начальной позицией
    return Player(20, 40)

def test_collision_with_map_x(environment, player):
    # Устанавливаем движение игрока по оси x
    player.dx = 5
    player.dy = 0

    # Проверяем столкновение с картой
    collided = player.collision_with_map(environment)

    # Проверяем, что игрок останавливается при столкновении с блоком
    assert player.dx == 0, "Player should stop moving right when colliding with a block"
    # Проверяем, что вертикального столкновения нет
    assert not collided, "There should be no vertical collision"

def test_collision_with_map_y_top(environment, player):
    # Устанавливаем движение игрока по оси y вверх
    player.dx = 0
    player.dy = -5

    # Проверяем столкновение с картой
    collided = player.collision_with_map(environment)

    # Проверяем, что вертикальная скорость игрока сбрасывается до 0 после столкновения
    assert player.speed_y == 0, "Player's vertical speed should be reset to 0 after colliding with the top of a block"
    # Проверяем, что столкновения с землей нет
    assert collided, "There should be no ground collision"

def test_collision_with_map_y_bottom(environment, player):
    # Устанавливаем движение игрока по оси y вниз
    player.dx = 0
    player.dy = 5

    # Проверяем столкновение с картой
    collided = player.collision_with_map(environment)

    # Проверяем, что вертикальная скорость игрока сбрасывается до 0 после столкновения
    assert player.speed_y == 0, "Player's vertical speed should be reset to 0 after colliding with the bottom of a block"
    # Проверяем, что столкновение с землей есть
    assert collided, "There should be a ground collision"

def test_no_collision(environment, player):
    # Создаем другую тестовую карту данных
    data = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    environment = Environment(data)
    # Устанавливаем движение игрока по осям x и y
    player.dx = 5
    player.dy = -5

    # Проверяем отсутствие столкновений
    collided = player.collision_with_map(environment)

    # Проверяем, что столкновений нет
    assert not collided, "There should be no collision"

"""
    Тест загрузки базы данных
"""
@pytest.fixture
def environment_map():
    # Определение размера квадрата
    global SQUARE_SIZE
    SQUARE_SIZE = 20
    global water_group, door_group, coin_group, fish_group
    # Создание фиктивных групп спрайтов
    water_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    fish_group = pygame.sprite.Group()
    
    # Создание тестовой карты данных
    data = [
        [1, 1, 1, 1, 1],
        [1, 1, 0, 3, 1],
        [1, 4, 0, 5, 1],
        [1, 6, 3, 1, 1]
    ]

    return Environment(data, water_group, door_group, coin_group, fish_group)

def test_right_blocks_position(environment_map):
    # Проверка количества блоков
    assert len(environment_map.square_list) == 13, "There should be exactly 13 blocks"
    
    # Проверка позиции и размера блока
    block = environment_map.square_list[1]
    assert block[1].x == 1 * SQUARE_SIZE, "Block x position is incorrect"
    assert block[1].y == 0, "Block y position is incorrect"
    assert block[1].width == SQUARE_SIZE, "Block width is incorrect"
    assert block[1].height == SQUARE_SIZE, "Block height is incorrect"

def test_right_water_position(environment_map):
    # Проверка количества воды
    assert len(water_group) == 2, "There should be exactly 2 water"
    
    # Проверка позиции воды
    water = next(iter(water_group))
    assert water.rect.x == 3 * SQUARE_SIZE, "Water x position is incorrect"
    assert water.rect.y == 1 * SQUARE_SIZE + (SQUARE_SIZE // 2), "Water y position is incorrect"

def test_right_doors_position(environment_map):
    # Проверка количества дверей
    assert len(door_group) == 1, "There should be exactly 1 door"
    
    # Проверка позиции двери
    door = next(iter(door_group))
    assert door.rect.x == 1 * SQUARE_SIZE, "Door x position is incorrect"
    assert door.rect.y == 2 * SQUARE_SIZE, "Door y position is incorrect"

def test_right_coins_position(environment_map):
    # Проверка количества монет
    assert len(coin_group) == 1, "There should be exactly 1 coin"
    
    # Проверка позиции монеты
    coin = next(iter(coin_group))
    assert coin.rect.x == 3 * SQUARE_SIZE, "Coin x position is incorrect"
    assert coin.rect.y == 2 * SQUARE_SIZE, "Coin y position is incorrect"

def test_right_fish_position(environment_map):
    # Проверка количества рыб
    assert len(fish_group) == 1, "There should be exactly 1 fish"
    
    # Проверка позиции рыбы
    fish = next(iter(fish_group))
    assert fish.rect.x == 1 * SQUARE_SIZE, "Fish x position is incorrect"
    assert fish.rect.y == 3 * SQUARE_SIZE, "Fish y position is incorrect"

if __name__ == "__main__":
    pytest.main()
