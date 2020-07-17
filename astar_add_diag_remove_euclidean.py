import pygame
import math
from queue import PriorityQueue
import time

###########################################################
#   This is built onto the astar.py file.
#	Added: 
#	Ability for the path to move diagonally through open areas.
#	Algorithm now handles different distances between two Spots
#


###################################################
### Constant Definitions                        ###
###################################################
WIDTH = 1000

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


# Defining the display window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


###################################################
### Class Definitions                           ###
###################################################

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
			if not grid[self.row][self.col + 1].is_barrier() and not grid[self.row + 1][self.col].is_barrier():
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





###################################################
### A* path finding algorithm related functions ###
###################################################
def h(p1, p2, use_euclidean):
	# Calculates the distance between two points using Euclidean or Manhattan 
	# determined by the bool use_euclidean
	x1, y1 = p1
	x2, y2 = p2

	if use_euclidean:
		distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) # Note: requires 3 operations
	else:
		distance = abs(x1 - x2) + abs(y1 - y2) # Note: requires 2 operations

	return distance



def reconstruct_path(came_from, current, draw, start):
	while current in came_from:
		current = came_from[current]
		if current != start:
			current.make_path()
		draw() # Can comment this function out if you do not want the path to be drawn one by one



def a_star_pathfind(draw, grid, start, end, use_euclidean):
	shortest_path = [] # What we are returning

	count = 0 # Used for tiebreakers when determining which spot to visit next
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {} # Keeps track of our current path from the start to the current spot

	# a spots g_score is the shortest determined path from the starting spot to this spot
	g_score = {spot: float("inf") for row in grid for spot in row} # Initialize a hash to track the g_scores of the spots
	g_score[start] = 0

	# a spots f_score is the spots g_score + their Euclidean or Manhattan distance to the end spot
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos(), use_euclidean)

	# because we are unable to see if a spot is in a PriorityQueue we use open_set_hash to track which ones are
	open_set_hash = {start}

	while not open_set.empty():

		# If the user wants to exit before the algorithm has finished executing then they can quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		# We get our next spot determined by the spot with the minimum f_score and if this is tied than the minimum count
		current = open_set.get()[2]
		# Remove this element from the open set
		open_set_hash.remove(current)

		# If our current spot is the end spot than we have found the shortest path and we can construct our path
		if current == end:
			reconstruct_path(came_from, current, draw, start)
			for row in grid:
				for spot in row:
					if spot.is_path():
						shortest_path.append(spot)

			return shortest_path

		for neighbour in current.neighbours:
			# Since we are traverse along a grid then our distances are all 1
			# 	(If it was desired we could implement uneven distances in the update_neighbours())
			temp_g_score = g_score[current] + current.neighbours[neighbour]

			# We then check if the path from the starting spot to the neighbour is shorter if it traverses through
			# our current spot, if so it replaces the neighbours current g_score with the new temp_g_score
			if temp_g_score < g_score[neighbour]:
				# We update the information of the neighbour
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				# It is unnecessary for use to check if the old f_score < the new f_score as h(neighbour, end) is 
				# equal in both and since we know that temp_g_score < g_score then the new f_score < the old f_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos(), use_euclidean)

				# If the neighbour is not in the open set than we add the neighbour to the PriorityQueue (open_set) for it to be considered
				# and if its f_score is every the lowest of all the elements then it will be explored
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()

		draw() # Can comment this function out if you do not want the algorithm to be visualized as it goes

		# We have now traversed this spot and we will close it to prevent us revisiting it again and going into an infinite loop
		if current != start:
			current.make_closed()

	# If we have no more spots in the open_set then we have traversed to all possible spots and there is no path
	return shortest_path





###################################################
### Display and grid editing related  functions ###
###################################################
def make_grid(rows, width):
	# Creates a clear rows x rows sized grid of empty spots
	grid = []
	gap = width // rows # gap determines the size of each spot for when it is drawn

	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i,j,gap,rows)
			grid[i].append(spot)

	return grid



def reset_grid(grid):
	# This is used to clear the grid of all non-barrier, start or end spots
	for row in grid:
		for spot in row:
			if (spot.is_path() or spot.is_open() or spot.is_closed()):
				spot.reset()


def reset_end(grid, end):
	# Temporary fix for issue that causes the end to be coloured as part of the path
	# Called after the path is drawn to make the end the correct colour
	row,col = end.get_pos()
	grid[row][col].make_end()



def draw_grid(win, rows, width):
	# Iterates through the grid drawing the grid lines
	gap = width // rows;
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # Horizontal lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # Vertical lines



def draw_spots(win,grid):
	# Iterates through the grid drawing all the spots
	for row in grid:
		for spot in row:
			spot.draw(win)


def draw(win, grid, rows, width):
	# Covers old frame
	win.fill(WHITE)

	draw_spots(win,grid) # Draw spots
	draw_grid(win, rows, width) # Draw grid lines

	pygame.display.update() # Update display



def get_clicked_pos(pos, rows, width):
	# Determines the mouses position when clicked
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col



def count_traverse_points(grid):
	# Iterates through the grid counting the number of traversed spots
	point_count = 0
	for row in grid:
		for spot in row:
			if spot.is_closed():
				point_count += 1

	return point_count



def count_path_points(grid):
	point_count = 0
	for row in grid:
		for spot in row:
			if spot.is_path():
				point_count += 1

	return point_count


def a_star_main(win, width):
	# Define constants and variables
	ROWS = 25
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True

	t0 = 0
	times = []
	point_counts = []
	path_counts = []
	found_path = {}

	while run:
		# Draws each frame
		draw(win, grid, ROWS, width)

		# Checks for user input
		for event in pygame.event.get():
			# Exits program
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # Triggers on left mouse click
				pos = pygame.mouse.get_pos() # Get mouses position
				row, col = get_clicked_pos(pos, ROWS, width) # Determine the corresponding row col on grid
				spot = grid[row][col]

				if not start and spot != end:
					# If we do not have a start we set the spot to the start
					#	 ( Can't be overridden by barrier or end spot)
					start = spot
					start.make_start()

				elif not end and spot != start:
					# If we do not have an end we set the spot to the end
					#	 ( Can't be overridden by barrier or start spot)
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					# Turn an empty spot to a barrier
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # Triggers on right mouse click
				pos = pygame.mouse.get_pos() # Get mouses position
				row, col = get_clicked_pos(pos, ROWS, width) # Determine the corresponding row col on grid

				# Turn any spot back to an empty spot
				spot = grid[row][col]
				spot.reset()

				if spot == start:
					# If the start is reset then reset the start
					start = None
				elif spot == end:
					# If the end is reset then reset the end
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end: # Triggers if spacebar is pressed

					# Determine the neighbours of each spot for use in the algorithm
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)

					# t0 = time.time() # Start timer for process

					# a_star_pathfind(lambda: draw(win, grid, ROWS, width), grid, start, end, True)
					
					#times.append(time.time() - t0) # Record time taken
					#point_counts.append(count_traverse_points(grid)) # Record spots traversed
					#path_counts.append(count_path_points(grid)) # Record path length

					#reset_end(grid, end)
					#draw(win, grid, ROWS, width)

					#time.sleep(2.5)
					#reset_grid(grid) # Reset all non-barrier, start or end spots for visualization purposes

					t0 = time.time() # Start timer for process
					found_path = a_star_pathfind(lambda: draw(win, grid, ROWS, width), grid, start, end, False)
					times.append(time.time() - t0) # Record time taken
					point_counts.append(count_traverse_points(grid)) # Record spots traversed
					path_counts.append(count_path_points(grid)) # Record path length

					reset_end(grid, end)
					draw(win, grid, ROWS, width)

				elif event.key == pygame.K_c: # Triggers if the 'c' key is pressed
					# Resets the board to be only empty spots
					start = None
					end = None
					grid = make_grid(ROWS, width)

				elif event.key == pygame.K_ESCAPE: # Alternative way to exit program
					run = False

	pygame.quit()

	# Outputs times and spot counts in alternating from Euclidean to Manhattan
	for t in times:
		print(t)
	for p in point_counts:
		print(p)
	for l in path_counts:
		print(l)

	return found_path



###################################################
### Code that is too be run                     ###
###################################################
shortest_path = a_star_main(WIN, WIDTH)

shortest_path.sort()