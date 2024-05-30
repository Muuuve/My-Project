import unittest
import pygame
from pygame.locals import *
from main import Player, Environment, bubble_sort, SQUARE_SIZE, PLAYER_WIDTH, PLAYER_HEIGHT

class TestBubbleSort(unittest.TestCase):

    def setUp(self):
        self.data = [('Result', '2024-05-29 21:31:08.858149', 18),
                     ('Result', '2024-05-29 21:31:55.009608', 15),
                     ('Result', '2024-05-29 21:33:08.846203', 5),
                     ('Result', '2024-05-29 21:34:25.103373', 18),
                     ('Result', '2024-05-29 21:35:10.472828', 16),
                     ('Result', '2024-05-29 21:35:23.823227', 1)]

    def test_bubble_sort_positive(self):
        bubble_sort(self.data)
        expected_result = [('Result', '2024-05-29 21:31:08.858149', 18),
                           ('Result', '2024-05-29 21:34:25.103373', 18),
                           ('Result', '2024-05-29 21:35:10.472828', 16),
                           ('Result', '2024-05-29 21:31:55.009608', 15),
                           ('Result', '2024-05-29 21:33:08.846203', 5),
                           ('Result', '2024-05-29 21:35:23.823227', 1)]
        self.assertEqual(self.data, expected_result)

    def test_bubble_sort_invalid_data(self):
        self.data.append(('Result', '2024-05-29 21:34:25.103373'))
        with self.assertRaises(IndexError):
            bubble_sort(self.data)

class TestCollisionWithMap(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.environment = Environment([
            [1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1]
        ])
        self.player = Player(50, 100)

    def test_collision_with_map_x(self):
        self.player.dx = 5
        self.player.dy = 0
        collided = self.player.collision_with_map(self.environment)
        self.assertEqual(self.player.dx, 0)
        self.assertFalse(collided)

    def test_collision_with_map_y_top(self):
        self.player.dx = 0
        self.player.dy = -5
        collided = self.player.collision_with_map(self.environment)
        self.assertEqual(self.player.speed_y, 0)
        self.assertTrue(collided)

    def test_collision_with_map_y_bottom(self):
        self.player.dx = 0
        self.player.dy = 5
        collided = self.player.collision_with_map(self.environment)
        self.assertEqual(self.player.speed_y, 0)
        self.assertTrue(collided)

    def test_no_collision(self):
        data = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
        ]
        self.environment = Environment(data)
        self.player.dx = 5
        self.player.dy = -5
        collided = self.player.collision_with_map(self.environment)
        self.assertFalse(collided)

class TestEnvironmentMap(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.water_group = pygame.sprite.Group()
        self.door_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.fish_group = pygame.sprite.Group()
        
        # Создание тестовой карты данных
        self.data = [
            [1, 1, 1, 1, 1],
            [1, 1, 0, 3, 1],
            [1, 4, 0, 5, 1],
            [1, 6, 3, 1, 1]
        ]
        self.environment = Environment(self.data, self.water_group, self.door_group, self.coin_group, self.fish_group)

    def test_right_blocks_position(self):
        # Проверка количества блоков
        self.assertEqual(len(self.environment.square_list), 13, "There should be exactly 13 blocks")
        
        # Проверка позиции и размера блока
        block = self.environment.square_list[1]
        self.assertEqual(block[1].x, 1 * SQUARE_SIZE, "Block x position is incorrect")
        self.assertEqual(block[1].y, 0, "Block y position is incorrect")
        self.assertEqual(block[1].width, SQUARE_SIZE, "Block width is incorrect")
        self.assertEqual(block[1].height, SQUARE_SIZE, "Block height is incorrect")

    def test_right_water_position(self):
        # Проверка количества воды
        self.assertEqual(len(self.water_group), 2, "There should be exactly 2 water")
        
        # Проверка позиции воды
        water = next(iter(self.water_group))
        self.assertEqual(water.rect.x, 3 * SQUARE_SIZE, "Water x position is incorrect")
        self.assertEqual(water.rect.y, 1 * SQUARE_SIZE + (SQUARE_SIZE // 2), "Water y position is incorrect")

    def test_right_doors_position(self):
        # Проверка количества дверей
        self.assertEqual(len(self.door_group), 1, "There should be exactly 1 door")
        
        # Проверка позиции двери
        door = next(iter(self.door_group))
        self.assertEqual(door.rect.x, 1 * SQUARE_SIZE, "Door x position is incorrect")
        self.assertEqual(door.rect.y, 2 * SQUARE_SIZE, "Door y position is incorrect")

    def test_right_coins_position(self):
        # Проверка количества монет
        self.assertEqual(len(self.coin_group), 1, "There should be exactly 1 coin")
        
        # Проверка позиции монеты
        coin = next(iter(self.coin_group))
        self.assertEqual(coin.rect.x, 3 * SQUARE_SIZE, "Coin x position is incorrect")
        self.assertEqual(coin.rect.y, 2 * SQUARE_SIZE, "Coin y position is incorrect")

    def test_right_fish_position(self):
        # Проверка количества рыб
        self.assertEqual(len(self.fish_group), 1, "There should be exactly 1 fish")
        
        # Проверка позиции рыбы
        fish = next(iter(self.fish_group))
        self.assertEqual(fish.rect.x, 1 * SQUARE_SIZE, "Fish x position is incorrect")
        self.assertEqual(fish.rect.y, 3 * SQUARE_SIZE, "Fish y position is incorrect")

if __name__ == '__main__':
    unittest.main()