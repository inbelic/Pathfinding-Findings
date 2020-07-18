import pygame
import math
from queue import PriorityQueue
import Spot


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





#################################
### A* path finding algorithm ###
#################################
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