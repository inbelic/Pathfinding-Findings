import visualization as vs
import pygame
import math

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


# Defining the display window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


###################################################
### Code that is too be run                     ###
###################################################
shortest_path = vs.a_star_main(WIN, WIDTH)

shortest_path.sort()