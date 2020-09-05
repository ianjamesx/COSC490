import random
import numpy as np
import pygame

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location, and space between grids
GRIDX = 40
GRIDY = 40
gridCount = 11

WINDOWX = 500
WINDOWY = 500
SPACING = 5

FPS = 60
WINDOW = [WINDOWX, WINDOWY]
screen = pygame.display.set_mode(WINDOW)

grid = []
 
#add an array nested in array of grids
def initGrid():
	for row in range(gridCount):
		grid.append([])
		for column in range(gridCount):
			grid[row].append(0)

def setBounds():
	for row in range(gridCount):
		for column in range(gridCount):
			if isBound(row, column):
				grid[row][column] = -1

#determine if grid at this row/col is a bound grid (end of map)
def isBound(row, col):
	if (col == 0 or col == gridCount-1):
		return True
	if (row == 0 or row == gridCount-1):
		return True
	return False

def drawGrid():
	for row in range(gridCount):
		for column in range(gridCount):

			#color outside grids red to represent bounds
			if isBound(row, column):
				gridColor = RED
			else:
				gridColor = WHITE

			pygame.draw.rect(screen, gridColor,
			[(SPACING + GRIDX) * column + SPACING,
			(SPACING + GRIDY) * row + SPACING,
			GRIDX,
			GRIDY])


initGrid()
setBounds()
 
# Loop until the user clicks the close button.
done = False

#for adjusting FPS
clock = pygame.time.Clock()
 
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    drawGrid()

    clock.tick(FPS)
 
    pygame.display.flip()

pygame.quit()

'''
class DecisionFactory:
    def __init__(self, name='Davros'):
	self.name = name
	self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
        self.results = [ 'success', 'failure', 'portal' ]
        self.last_result = self.results[0]
        self.last_direction = 'wait'

	# Note: we have relativistic coordinates recorded here, since the map
	#   is relative to the player's first known and recorded position:
	# self.state.pos = (0, 0)


    def get_decision(self, verbose = True):
	return self.random_direction()


    def random_direction(self):
	#r = random.randint(0,4) # Includes wait state
	r = random.randint(1,4) # Does NOT include wait state

	# Update last direction to be the one just selected:
	self.last_direction = self.directions[r]

        return self.directions[r]	


    def put_result(self, result):
        self.last_result = result

'''