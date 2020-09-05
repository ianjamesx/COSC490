import random
import numpy as np
import pygame

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location, and space between grids
GRIDX = 40
GRIDY = 40

WINDOWX = 500
WINDOWY = 500
SPACING = 5

WINDOW = [WINDOWX, WINDOWY]
screen = pygame.display.set_mode(WINDOW)
 
# This sets the margin between each cell

#init grid
grid = []
 
def initGrid():
	for row in range(10):
		# Add an empty array that will hold each cell
		# in this row
		grid.append([])
		for column in range(10):
			grid[row].append(0)  # Append a cell

def drawGrid():
	for row in range(10):
		for column in range(10):
			color = WHITE
			if grid[row][column] == 1:
				color = GREEN
			pygame.draw.rect(screen, color,
			[(SPACING + GRIDX) * column + SPACING,
			(SPACING + GRIDY) * row + SPACING,
			GRIDX,
			GRIDY])


initGrid()
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1
 
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
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
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