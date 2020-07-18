import pygame
import math 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQOISE = (64, 224, 208)

# Spot class definition
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col

		# Used to keep track of where to draw on screen
		self.x = row * width
		self.y = col * width
		self.width = width

		self.color = WHITE

		self.neighbours = {}
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQOISE

	def is_path(self):
		return self.color == PURPLE

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = TURQOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self,win):
		# Draws itself to the display
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbours(self, grid):
		# Initialize variable
		self.neighbours = {}

		# Determine if spots to the North, South, East and West are valid respectively
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #North
			self.neighbours[grid[self.row + 1][self.col]] = 1

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #South
			self.neighbours[grid[self.row - 1][self.col]] = 1

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #East
			self.neighbours[grid[self.row][self.col + 1]] = 1

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #West
			self.neighbours[grid[self.row][self.col - 1]] = 1

		# We want to let the path go diagonally if the two spots are both not barriers, to avoid going through walls but
		# let the path me more efficient when traversing open areas

		# Distance on the diagonal should be the root of 2 but for simplicity we will set it to 1.75.
		# We just need the distance to be less than 2 to make it more efficient than going left then down etc
		# and we need the distance to be more than 1 so that we don't introduce zig-zagging to our path

		if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): #North East
			#Check if North or East spots are barriers
			if not grid[self.row][self.col + 1].is_barrier() or not grid[self.row + 1][self.col].is_barrier():
				self.neighbours[grid[self.row + 1][self.col + 1]] = 1.75

		if self.row > 0 and self.col > 0  and not grid[self.row - 1][self.col - 1].is_barrier(): #South West
			#Check if South or West spots are barriers
			if not grid[self.row][self.col - 1].is_barrier() or not grid[self.row - 1][self.col].is_barrier():
				self.neighbours[grid[self.row - 1][self.col - 1]] = 1.75

		if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier(): #South East
			#Check if South or East spots are barriers
			if not grid[self.row][self.col + 1].is_barrier() or not grid[self.row - 1][self.col].is_barrier():
				self.neighbours[grid[self.row - 1][self.col + 1]] = 1.75

		if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier(): #North West
			#Check if North or West spots are barriers
			if not grid[self.row + 1][self.col].is_barrier() or not grid[self.row][self.col - 1].is_barrier():
				self.neighbours[grid[self.row + 1][self.col - 1]] = 1.75


	def __lt__ (self, other):
		return ((self.col, self.row) <
                (other.col, other.row))		