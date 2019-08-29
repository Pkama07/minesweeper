import pygame
import time
from random import randint

pygame.init()

unopened_square = pygame.transform.scale(pygame.image.load("Assets/Images/unopened_square.png"), (40, 40))
bomb = pygame.transform.scale(pygame.image.load("Assets/Images/bomb.png"), (40, 40))
flag = pygame.transform.scale(pygame.image.load("Assets/Images/flag.png"), (40, 40))
explosion = pygame.transform.scale(pygame.image.load("Assets/Images/explosion.png"), (800, 600))
win_x = 1000
win_y = 680
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
open_sound = pygame.mixer.Sound("Assets/Sounds/open.wav")
explosion_sound = pygame.mixer.Sound("Assets/Sounds/explosion.wav")


class Field(object):


	def __init__(self, click_x, click_y):
		self.x_dim = [(x*40-40, x*40) for x in range(9, 27)]
		self.y_dim = [(y*40-40, y*40) for y in range(1, 19)]
		initial_coords = self.convert_click(click_x, click_y, self.x_dim, self.y_dim)
		rows_and_squares = self.make_shape(initial_coords[0], initial_coords[1])
		self.squares = rows_and_squares[1]
		self.rows = self.fill_field(self.place_mines(rows_and_squares[0]))
		self.flags = [[0 for num in range(17)] for num in range(17)]
		self.bombs = [[0.0 for num in row if num == 10] for row in self.rows]


	def fill_field(self, rows):
		for y in range(17):
			for x in range(17):
				if rows[y][x] == 10:
					for possible_x, possible_y in ((x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)):
						if 0 <= possible_x <= 16 and 0 <= possible_y <= 16:
							if not rows[possible_y][possible_x] == 10:
								rows[possible_y][possible_x] += 1
		return rows


	def place_mines(self, rows):
		mine_cnt = 40
		while mine_cnt > 0:
			rand_x = randint(0, 16)
			rand_y = randint(0, 16)
			if not type(rows[rand_y][rand_x]) is float:
				rows[rand_y][rand_x] = 10
				mine_cnt -= 1
		return rows



	def convert_click(self, x, y, x_dim, y_dim):
		x_index = 0
		y_index = 0
		match_found = False
		count = 0
		while not match_found:
			if x_dim[count][0] <= x < x_dim[count][1]:
				x_index = count
				match_found = True
			count += 1
		match_found = False
		count = 0
		while not match_found:
			if y_dim[count][0] <= y < y_dim[count][1]:
				y_index = count
				match_found = True
			count += 1
		return [x_index, y_index]


	def make_shape(self, x, y):
		rows = [[0 for num in range(17)] for num in range(17)]
		squares = rows
		shapes = {
					"shape_1": [(x-1, y), (x-1, y-1), (x-1, y+1), (x, y+1), (x, y), (x, y-1), (x, y-2), (x+1, y+1), (x+1, y), (x+1, y-1), (x+1, y-2), (x+2, y+1), (x+2, y), (x+2, y-1), (x+2, y-2)],
					"shape_2": [(x-1, y), (x, y+1), (x, y), (x, y-1), (x, y-2), (x+1, y+2), (x+1, y+1), (x+1, y), (x+1, y-1), (x+1, y-2), (x+2, y), (x+2, y-1)],
					"shape_3": [(x-2, y), (x-2, y+1), (x-1, y), (x-1, y+1), (x, y-1), (x, y), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1), (x+1, y+2), (x+2, y-1), (x+2, y), (x+2, y+1), (x+2, y+2), (x+3, y-1), (x+3, y), (x+3, y+1), (x+3, y+2)]
												}
		shape_names = ["shape_1", "shape_2", "shape_3"]
		shape_index = randint(0, 2)
		for point in shapes[shape_names[shape_index]]:
			if 0 <= point[0] <= 16 and 0 <= point[1] <= 16:
				rows[point[1]][point[0]] = 0.0
				squares[point[1]][point[0]] = 0.0
		return [rows, squares]


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(text, size, place, color, font):
    font = pygame.font.Font(font, size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = place
    win.blit(text_surf, text_rect)


def draw_main_menu():
	no_x = [num for num in range(25) if 8 <= num <= 16]
	no_y = [2, 3]
	win.fill((211, 211, 211))
	for y in range(int(win_y/40)):
		for x in range(int(win_x/40)):
			if not x in no_x or not y in no_y:
				win.blit(unopened_square, (x*40, y*40))
	if check_play():
		pygame.draw.rect(win, (211, 211, 211), (440, 360, 120, 120))
	draw_text("Minesweeper", 85, (win_x/2+1, win_y/2-210), (0, 0, 0), "Assets/Font/ostrich-regular.ttf")
	draw_text("Play", 50, (win_x/2, win_y/2+80), (0, 0, 0), "Assets/Font/ostrich-regular.ttf")
	pygame.display.update()


def check_play():
	if 440 <= pygame.mouse.get_pos()[0] <= 560 and 360 <= pygame.mouse.get_pos()[1] <= 480:
		return True
	else:
		return False


in_main_menu = True

while in_main_menu:
	draw_main_menu()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if 440 <= pygame.mouse.get_pos()[0] <= 560 and 360 <= pygame.mouse.get_pos()[1] <= 480:
				while 440 <= pygame.mouse.get_pos()[0] <= 560 and 360 <= pygame.mouse.get_pos()[1] <= 480:
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONUP:
							in_main_menu = False


def draw_first():
	win.fill((211, 211, 211))
	win.blit(pygame.transform.scale(flag, (80, 80)), (80, 200))
	for x in range(8, 25):
		for y in range(0, 17):
			win.blit(unopened_square, (x*40, y*40))
	draw_text(str(40), 60, (200, 245), (255, 0, 0), "Assets/Font/ostrich-regular.ttf")
	pygame.display.update()


on_first_click = True
while on_first_click:
	draw_first()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if 320 <= pygame.mouse.get_pos()[0] <= 1000:
				open_sound.play()
				(x, y) = pygame.mouse.get_pos()
				on_first_click = False

field = Field(x, y)

def draw_game():
	win.fill((211, 211, 211))
	win.blit(pygame.transform.scale(flag, (80, 80)), (80, 200))
	for y in range(17):
		for x in range(8, 25):
			if type(field.squares[y][x-8]) is float:
				if not field.rows[y][x-8] == 10:
					draw_text(str(int(field.rows[y][x-8])), 30, (x*40+20, y*40+20), (0, 0, 0), "Assets/Font/ostrich-regular.ttf")
				else:
					win.blit(bomb, (x*40, y*40))
			else:
				win.blit(unopened_square, (x*40, y*40))
	flag_count = 40
	for y in range(17):
		for x in range(8, 25):
			if type(field.flags[y][x-8]) is float:
				win.blit(flag, (x*40, y*40))
				flag_count -= 1
	draw_text(str(flag_count), 60, (200, 245), (255, 0, 0), "Assets/Font/ostrich-regular.ttf")


in_game = True
while in_game:
	draw_game()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			(x, y) = pygame.mouse.get_pos()
			if 320 <= x <= 1000:
				clicked_point = field.convert_click(x, y, field.x_dim, field.y_dim)
				if event.button == 1:
					if type(field.flags[clicked_point[1]][clicked_point[0]]) is int:
						if not field.rows[clicked_point[1]][clicked_point[0]] == 10:
							open_sound.play()
							field.squares[clicked_point[1]][clicked_point[0]] = float(field.squares[clicked_point[1]][clicked_point[0]])
						else:
							for y in range(17):
								for x in range(17):
									if field.rows[y][x] == 10:
										field.squares[y][x] = float(field.squares[y][x])
										in_game = False
										in_game_over = True
				elif event.button == 3:
					if type(field.flags[clicked_point[1]][clicked_point[0]]) is int:
						field.flags[clicked_point[1]][clicked_point[0]] = 0.0
					elif type(field.flags[clicked_point[1]][clicked_point[0]]) is float:
						field.flags[clicked_point[1]][clicked_point[0]] = 0
	if field.flags == field.bombs:
		in_win = True
	pygame.display.update()
for row in field.flags:
	print(row)
count = 0
while in_game_over:
	draw_game()
	while count == 0:
		explosion_sound.play()
		count += 1
	win.blit(explosion, (100, 40))
	draw_text("Game Over", 200, (500, 340), (0, 0, 0), "Assets/Font/ostrich-regular.ttf")
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

while in_win:
	draw_game()
	draw_text("YOU WIN", 200, (500, 340), (0, 0, 0), "Assets/Font/ostrich-regular.ttf")
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()