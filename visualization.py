import pygame
import math
import time
import Spot as S
import a_star_algorithm as asg

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
			spot = S.Spot(i,j,gap,rows)
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
		pygame.draw.line(win, S.GREY, (0, i * gap), (width, i * gap)) # Horizontal lines
		for j in range(rows):
			pygame.draw.line(win, S.GREY, (j * gap, 0), (j * gap, width)) # Vertical lines



def draw_spots(win,grid):
	# Iterates through the grid drawing all the spots
	for row in grid:
		for spot in row:
			spot.draw(win)


def draw(win, grid, rows, width):
	# Covers old frame
	win.fill(S.WHITE)

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



###############################################
### Main loop for visualization and display ###
###############################################
def a_star_main(win, width):
	# Define constants and variables
	ROWS = 50
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
					found_path = asg.a_star_pathfind(lambda: draw(win, grid, ROWS, width), grid, start, end, False)
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