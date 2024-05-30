import pygame
import json
import csv
from datetime import datetime
from os import path

# Размеры окна
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Игровые переменные
SQUARE_SIZE = 50
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
MAX_LEVEL = 5

# Цвета
WHITE_COLOR = (255, 255, 255)

# Группа для блоков воды
water_group = pygame.sprite.Group()

# Группа для дверей
door_group = pygame.sprite.Group()

# Группа для монет
coin_group = pygame.sprite.Group()

# Группа для рыб
fish_group = pygame.sprite.Group()

# Функция для текста
def text(text, font, text_color, x, y):
	image = font.render(text, True, text_color)
	screen.blit(image, (x, y))

# Функция для загрузки уровней
def restart_level(level, player):
	player.restart(100, SCREEN_HEIGHT - 130)
	water_group.empty()
	door_group.empty()
	coin_group.empty()
	fish_group.empty()

	# Создание окружения уровня
	if path.exists('levels/level' + str(level)):
		level_file = open('levels/level' + str(level), 'r')
		environment_data = json.load(level_file)
	environment = Environment(environment_data)

	# Монета в левом верхнем углу
	score_coin = Coin(SQUARE_SIZE // 2 - 10, SQUARE_SIZE // 2 - 5)
	coin_group.add(score_coin)

	# Сердце в правом верхнем углу
	heart = Fish(SCREEN_WIDTH - 100, SQUARE_SIZE // 2 - 5, 2)
	fish_group.add(heart)

	return environment

# Функция для сортировки csv файла от наибольшего результата к наименьшему
def bubble_sort(data):
    n = len(data)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if data[j][2] < data[j + 1][2]:
                data[j], data[j + 1] = data[j + 1], data[j]

# Класс для кнопок
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		# Какое-либо действие
		operation = False
		# Позиция курсора на экран
		position = pygame.mouse.get_pos()

		# Проверка нажатия
		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				operation = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, self.rect)

		return operation

# Класс для создания игрового персонажа
class Player():
	def __init__(self, x, y):
		self.restart(x, y)
		self.walking_fps = 20


	def collision_with_map(self, environment):
		# Проверка на стокновение c окружением
		for square in environment.square_list:
			# Столкновение по оси x
			if square[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
				self.dx = 0
				
			# Столкновение по оси y
			if square[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
				# Под блоком
				if self.speed_y < 0:
					self.dy = square[1].bottom - self.rect.top
					self.speed_y = 0
				# Над блоком
				elif self.speed_y >= 0:
					self.dy = square[1].top - self.rect.bottom
					self.speed_y = 0
					return True
		return False

	# Отрисовка игрового персонажа
	def update(self, game_over, environment, health):
		self.dx = 0
		self.dy = 0
		# global ealth

		if game_over == 0:

			# Управление персонажем
			key = pygame.key.get_pressed()
			if key[pygame.K_a]:
				self.dx -= 5
				self.counter += 5
				self.direction = -1

			if key[pygame.K_d]:
				self.dx += 5
				self.counter += 5
				self.direction = 1

			if key[pygame.K_w] and self.jump == False and self.is_grounded == True:
				self.speed_y = -15
				self.jump = True

			if key[pygame.K_w] == False:
				self.jump = False

			if key[pygame.K_a] == False and key[pygame.K_d] == False:
				self.counter = 0
				self.number = 0
				if self.direction == 1:
					self.image = self.images_r[self.number]
				if self.direction == -1:
					self.image = self.images_l[self.number]


			# Анимация движения влево или вправо
			if self.counter > self.walking_fps:
				self.counter = 0
				self.number += 1
				if self.number >= 3:
					self.number = 0
				if self.direction == 1:
					self.image = self.images_r[self.number]
				if self.direction == -1:
					self.image = self.images_l[self.number]

			# Гравитация
			self.speed_y += 1
			if self.speed_y > 10:
				self.speed_y = 10
			self.dy += self.speed_y


			self.is_grounded = self.collision_with_map(environment)

			# Проверка на столкновение с водой
			if pygame.sprite.spritecollide(self, water_group, False):
				if health[0] > 1:
					self.restart(100, SCREEN_HEIGHT - 130)

					# Монета в левом верхнем углу
					score_coin = Coin(SQUARE_SIZE // 2 - 10, SQUARE_SIZE // 2 - 5)
					coin_group.add(score_coin)

					# Сердце в правом верхнем углу
					heart = Fish(SCREEN_WIDTH - 100, SQUARE_SIZE // 2 - 5, 2)
					fish_group.add(heart)

					health[0] -= 1
				else:
					game_over = -1
					health[0] = 3

			# Проверка на прохождение уровня
			if pygame.sprite.spritecollide(self, door_group, False):
				game_over = 1

	        # Обновлённая позиция персонажа
			self.rect.x += self.dx
			self.rect.y += self.dy


		screen.blit(self.image, self.rect)

		return game_over

	def restart(self, x, y):
		self.images_r = []
		self.images_l = []
		self.number = 0
		self.counter = 0
		for i in range(1, 3+1):
			image_r = pygame.image.load('images/cat' + str(i) + '.png')
			image_r = pygame.transform.scale(image_r, (PLAYER_WIDTH, PLAYER_HEIGHT))
			image_l = pygame.transform.flip(image_r, True, False)
			self.images_r.append(image_r)
			self.images_l.append(image_l)
		self.image = self.images_r[self.number]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.speed_y = 0
		self.jump = False
		self.direction = 0
		self.is_grounded = False

# Класс для создания окружения уровня
class Environment():
	def __init__(self, data, water_group=water_group, door_group=door_group, coin_group=coin_group, fish_group=fish_group):
		self.square_list = []
		self.build_map(data, water_group, door_group, coin_group, fish_group)

	def build_map(self, data, water_group, door_group, coin_group, fish_group):
		# Загрузка изображений
		block_image = pygame.image.load('images/block.png')

		row_counter = 0
		for row in data:
			column_counter = 0
			for square in row:
				if square == 1:
					image = pygame.transform.scale(block_image, (SQUARE_SIZE, SQUARE_SIZE))
					image_rect = image.get_rect()
					image_rect.x = column_counter * SQUARE_SIZE
					image_rect.y = row_counter * SQUARE_SIZE
					square = (image, image_rect)
					self.square_list.append(square)
				if square == 3:
					water = Water(column_counter * SQUARE_SIZE, row_counter * SQUARE_SIZE + (SQUARE_SIZE // 2))
					water_group.add(water)
				if square == 4:
					door = Door(column_counter * SQUARE_SIZE, row_counter * SQUARE_SIZE)
					door_group.add(door)
				if square == 5:
					coin = Coin(column_counter * SQUARE_SIZE + (SQUARE_SIZE // 2), row_counter * SQUARE_SIZE + (SQUARE_SIZE // 2))
					coin_group.add(coin)
				if square == 6:
					fish = Fish(column_counter * SQUARE_SIZE + (SQUARE_SIZE // 2), row_counter * SQUARE_SIZE + (SQUARE_SIZE // 2), 1)
					fish_group.add(fish)
				column_counter += 1
			row_counter += 1


	# Отрисовка объектов
	def draw(self):
		for square in self.square_list:
			screen.blit(square[0], square[1])
		water_group.draw(screen)
		door_group.draw(screen)
		coin_group.draw(screen)
		fish_group.draw(screen)

# Класс для блоков воды
class Water(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('images/water.png')
		self.image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Класс для монеток
class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('images/coin.png')
		self.image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

# Класс для двери
class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('images/door.png')
		self.image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Класс для рыбок, которые будут увеличивать жизни персонажа и сердца в правом верхнем углу
class Fish(pygame.sprite.Sprite):
	def __init__(self, x, y, number):
		pygame.sprite.Sprite.__init__(self)
		if number == 1:
			image = pygame.image.load('images/fish.png')
		if number == 2:
			image = pygame.image.load('images/heart.png')
		self.image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

def main():
	# Инициализация Pygame
	pygame.init()

	game_over = 0
	menu = True
	level = 1
	score = 0
	health = 3

	# Создание окна
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Run, kitty, run!')

	# Счётчик кадров
	FPS = 60
	clock = pygame.time.Clock()

	# Загрузка изображений
	restart_image = pygame.image.load('images/restart.png')
	start_image = pygame.image.load('images/start.png')
	statistics_image = pygame.image.load('images/statistics.png')
	exit_image = pygame.image.load('images/exit.png')

	# Загрузка шрифта
	font_small = pygame.font.Font('images/font.ttf', 30)
	font_big = pygame.font.Font('images/font.ttf', 50)


	# Монета в левом верхнем углу
	score_coin = Coin(SQUARE_SIZE // 2 - 10, SQUARE_SIZE // 2 - 5)
	coin_group.add(score_coin)

	# Сердце в правом верхнем углу
	heart = Fish(SCREEN_WIDTH - 100, SQUARE_SIZE // 2 - 5, 2)
	fish_group.add(heart)

	# Создание окружения уровня
	if path.exists('levels/level' + str(level)):
		level_file = open('levels/level' + str(level), 'r')
		environment_data = json.load(level_file)
	environment = Environment(environment_data)

	# Создание кнопок
	restart_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, restart_image)
	start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 200, start_image)
	statistics_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, statistics_image)
	exit_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 200, exit_image)

	# Переменная для цикла игры
	running = True

	# Главный цикл игры
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		clock.tick(FPS)

		screen.fill((92, 148, 252))

		if menu == True:
			if start_button.draw() == True:
				menu = False
				# Создание игрового персонажа, задание его точки спавна
				player = Player(100, SCREEN_HEIGHT - 130)

				environment = restart_level(level, player)
			if statistics_button.draw() == True:
				with open('statistics.csv') as file:
					reader = csv.reader(file)
					data = list(reader)
					for row in data:
						row[0] = str(row[0])
						row[1] = str(row[1])
						row[2] = int(row[2])

				bubble_sort(data)

				i = 0
				for row in data:
					i += 1
					print(str(i) + '. ' + row[0] + ' ' + row[1] + ' ' + str(row[2]))
	    				
			if exit_button.draw() == True:
				running = False
		else:
			environment.draw()

			if game_over == 0:
				#Обновление количества монет
				if pygame.sprite.spritecollide(player, coin_group, True):
					score += 1
				if pygame.sprite.spritecollide(player, fish_group, True):
					health += 1
				text('X ' + str(score), font_small, WHITE_COLOR, SQUARE_SIZE - 10, 10)
				text('X ' + str(health), font_small, WHITE_COLOR, SCREEN_WIDTH - 70, 10)



			health = list([health])

			game_over = player.update(game_over, environment, health)
			health = health[0]
			# В случае проигрыша
			if game_over == -1:
				text("Let's try this level again!", font_big, WHITE_COLOR, (SCREEN_WIDTH // 2) - 400,  SCREEN_HEIGHT // 2)
				if restart_button.draw():
					environment_data = []
					environment = restart_level(level, player)
					game_over = 0
					score = 0
					health = 3

			# В случае прохождения уровня
			if game_over == 1:
				# Загружаем следующий уровень
				level += 1
				if level < MAX_LEVEL + 1:
					environment_data = []
					environment = restart_level(level, player)
					game_over = 0
					health = 3
				else:
					text('Great, you pass all levels!', font_big, WHITE_COLOR, (SCREEN_WIDTH // 2) - 410,  SCREEN_HEIGHT // 2)
					if restart_button.draw():
						with open('statistics.csv', 'a') as file:
							writer = csv.writer(file)
							writer.writerow(['Result', str(datetime.now()), int(score)])
						level = 1
						environment_data = []
						environment = restart_level(level, player)
						game_over = 0
						score = 0
						health = 3
					if exit_button.draw():
						exit()


		pygame.display.flip()


	# Завершение работы Pygame    
	pygame.quit()


if __name__ == '__main__':
	main()