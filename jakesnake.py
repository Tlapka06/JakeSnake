#!/usr/bin/env python3

import curses
import snakegame
import time
import appdirs
import os
import signal

# constants
LINES_RATIO = 1
COLS_RATIO = 2
KEYBINDINGS = {
	# UP
	curses.KEY_UP : snakegame.SnakeDirection.UP,
	ord("w") : snakegame.SnakeDirection.UP,
	# DOWN
	curses.KEY_DOWN : snakegame.SnakeDirection.DOWN,
	ord("s") : snakegame.SnakeDirection.DOWN,
	# LEFT
	curses.KEY_LEFT : snakegame.SnakeDirection.LEFT,
	ord("a") : snakegame.SnakeDirection.LEFT,
	# RIGHT
	curses.KEY_RIGHT : snakegame.SnakeDirection.RIGHT,
	ord("d") : snakegame.SnakeDirection.RIGHT,
	# exit
}
APP_NAME = "snake"
APP_AUTHOR = "jakubjanik"
DATA_PATH = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)

class GameData:
	"""Saves data of the game
	
	for now only hiscore"""
	def __init__(self, path):
		"""Initialize the object"""
		self.path = path
		
		if not os.path.exists(path):
			os.makedirs(path)
		
		self.load()
		
	def load(self):
		"""Load data to the object
		
		It is called during init"""
		self.hiscore = 0
		try:
			save = open(self.path + "/snake.dat", "r")
			self.hiscore = int(save.read())
			save.close()
		except ValueError:
			pass
		except FileNotFoundError:
			pass
	
	def save(self):
		"""Saves data back on the disk"""
		save = open(self.path + "/snake.dat", "w")
		save.write(str(self.hiscore))
		save.close()

def main(screen):
	"""Main function of the game"""
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	COLOR_SNAKE = curses.color_pair(1)
	COLOR_FOOD = curses.color_pair(2)
	COLOR_WALL = curses.color_pair(0)
	curses.curs_set(False)
	curses.raw()
	screen.nodelay(True)
	
	def draw_box(x, y, color):
		try:
			screen.addstr(x * LINES_RATIO, y * COLS_RATIO, "██", color)
		except:
			pass
	
	# game init
	data = GameData(DATA_PATH)
	snake = snakegame.Snake(curses.LINES // LINES_RATIO - 1, curses.COLS // COLS_RATIO - 1, length = 15)
	
	def exit_handler(signum, frame):
		data.save()
		exit()
	if os.name == "nt":
		signal.signal(signal.SIGBREAK, exit_handler)
	else:
		signal.signal(signal.SIGHUP, exit_handler)
	signal.signal(signal.SIGTERM, exit_handler)
	
	while True:
		#input
		user_input = screen.getch()
		if KEYBINDINGS.__contains__(user_input):
			snake.direction = KEYBINDINGS[user_input]
		elif user_input == ord("q"):
			snake.lost = True
		
		# update
		snake.move()
		
		# check hi-score
		if snake.score > data.hiscore:
			data.hiscore = snake.score
		
		# check if lost
		if snake.lost:
			screen.nodelay(False)
			#screen.clear()
			screen.addstr(2, 0, "You lost!")
			screen.addstr(curses.LINES - 1, 0, "Press enter to exit...")
			key = None
			while key != ord("\n") and key != ord("\r"):
				key = screen.getch()
			data.save()
			return
		
		# draw
		screen.clear()
		screen.addstr(0, 0, f"score: {snake.score}\nhi-score: {data.hiscore}")
		for i in snake.snake:
			draw_box(i.x, i.y, COLOR_SNAKE)
		draw_box(snake.food.x, snake.food.y, COLOR_FOOD)
		screen.refresh()
		
		# sleep
		time.sleep(0.25 / (1 + snake.score/5))

if __name__ == "__main__":
	curses.wrapper(main)
	print("Copyright © 2022 Jakub Janík")