#!/usr/bin/env python3

from collections import deque
import enum
import random

class Coordinates:
	"""Stores coordinates (x,y)"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __add__(self, object):
		return self.__class__(self.x + object.x, self.y + object.y)
	
	def __eq__(self, object):
		return self.x == object.x and self.y == object.y
	
	def __str__(self):
		return f"Coordinates(x: {self.x}, y: {self.y})"

class SnakeDirection(enum.Enum):
	"""Represents possible directions of the snake"""
	RIGHT = Coordinates(0,1)
	LEFT = Coordinates(0,-1)
	UP = Coordinates(-1,0)
	DOWN = Coordinates(1,0)

class Snake:
	"""Represents game itself
	
	Contains almost all game logic"""
	def __init__(self, width, height, length = 7):
		"""Initalize game with size of field and starting length of the snake"""
		self.__start_length = length
		self.__length = length
		self.__position = deque([Coordinates(random.randint(0, width), random.randint(0, height))])
		self.size = Coordinates(width, height)
		self.direction = SnakeDirection.RIGHT
		self.lost = False
		self.__generateFood()
	
	def move(self):
		"""Moves snake in set direction"""
		new_pos = self.__teleportOnEdge(self.__position[len(self.__position) - 1] + self.direction.value)
		if self.__intersects(new_pos):
			self.lost = True
			return
		self.__eatFood(new_pos)
		
		self.__position.append(new_pos)
		if len(self.__position) > self.__length:
			self.__position.popleft()
	
	def __intersects(self, position):
		for i in self.__position:
			if position == i:
				return True
		return False
	
	def __eatFood(self, position):
		if position == self.__food:
			self.__length += 1
			self.__generateFood()
	
	def __generateFood(self):
		self.__food = Coordinates(random.randint(0, self.size.x), random.randint(0, self.size.y))
		for i in self.__position:
			if self.__food == i:
				self.__generateFood()
				break
	
	def __teleportOnEdge(self, position):
		# check x for edge wraping
		if position.x < 0:
			position.x = self.size.x
		elif position.x > self.size.x:
			position.x = 0
		# check y for edge wraping
		if position.y < 0:
			position.y = self.size.y
		elif position.y > self.size.y:
			position.y = 0
		return position
	
	@property
	def score(self):
		"""Calculates score"""
		return self.__length - self.__start_length
	
	@property
	def snake(self):
		"""Returns copy of snakes body position"""
		return self.__position.copy()
	
	@property
	def food(self):
		"""Returns food position"""
		return self.__food