
import random
import numpy as np
class MapTiles:
    def __init__(self, x, y):
        self.coordinate = [x,y]

        self.minesweeper_number = 0
        self.successDirs = ['up', 'down', 'left', 'right']
        self.successPrio = [3, 3, 3, 3]
        self.priority = 3 #minesweeper number plus priority
class DecisionFactory:
    def __init__(self, name='Dude'):
        self.name = name
        self.directions = ['wait', 'up', 'down', 'right', 'left']
        self.results = ['success', 'failure', 'portal']
        self.order = ['up', 'down', 'right', 'left', 'down', 'up', 'left', 'right', 'wait']
        self.last_result = self.results[0]
        self.last_direction = 'wait'
        self.state_pos = [0, 0]
        self.last_nonStar = 'wait'
        self.map = np.array([])
        self.set_direction = 0
        self.map = np.append(self.map, MapTiles(0, 0))
        self.orderI = 0

    # Note: we have relativistic coordinates recorded here, since the map
    #   is relative to the player's first known and recorded position:
    # self.state.pos = (0, 0)

    def make_decision(self):  # Calculates priority and makes the decision
        flag = True
        maxvalue = 0
        dude = 0
        curr_tile = self.find_map_tile(self.state_pos[0], self.state_pos[1])
        for i in range(0, 4):  # Sets maxvalue to the highest priority of the adjacent tiles
            if flag:
                maxvalue = curr_tile.successPrio[i]
                flag = False
            if curr_tile.successPrio[i] > maxvalue:
                maxvalue = curr_tile.successPrio[i]
        for i in range(0, 4):  # Save the index of the highest priority tile
            if curr_tile.successPrio[i] == maxvalue:
                dude = i
                break
        curr_tile.successPrio[dude] -= 1  # Decreases the priority of the previous path
        self.update_priority(curr_tile.successDirs[dude])
        self.last_nonStar = curr_tile.successDirs[dude]
        if curr_tile.successDirs[dude] == 'up':
            self.last_nonStar = 'down'
        elif curr_tile.successDirs[dude] == 'down':
            self.last_nonStar = 'up'
        elif curr_tile.successDirs[dude] == 'left':
            self.last_nonStar = 'right'
        elif curr_tile.successDirs[dude] == 'right':
            self.last_nonStar = 'left'
        return curr_tile.successDirs[dude]

    def update_priority(self, direction):  # Updates the priority of the adjacent tile
        local_dude_x = self.state_pos[0]
        local_dude_y = self.state_pos[1]
        opp_direction = ''
        if direction == 'up':
            local_dude_y = self.state_pos[1]+1
            opp_direction = 'down'
        elif direction == 'down':
            local_dude_y = self.state_pos[1]-1
            opp_direction = 'up'
        elif direction == 'left':
            local_dude_x = self.state_pos[0]-1
            opp_direction = 'right'
        elif direction == 'right':
            local_dude_x = self.state_pos[0]+1
            opp_direction = 'left'
        curr_tile = self.find_map_tile(local_dude_x, local_dude_y)  # Tries to find the map tile
        for i in range(0, 4):  # Decreases the priority of the previous path
            if curr_tile.successDirs[i] == opp_direction:
                curr_tile.successPrio[i] -= 1

    def get_decision(self):  #
        direction = ''
        curr_tile = self.find_map_tile(self.state_pos[0], self.state_pos[1])
        self.orderI += 1
        if self.last_result == 'failure':
            self.orderI -= 1
            for i in range(0, 4):  # Sets negative priority for wall tiles so the dude doesnt go back
                if self.order[self.orderI - 1] == curr_tile.successDirs[i]:
                    curr_tile.successDirs[i] = "Dan"
                    curr_tile.successPrio[i] = -999
            self.orderI += 2
        if self.orderI >= 10:  # Rests the order of the star pattern algorithm
            self.orderI = 0
            direction = self.make_decision()  # call makes the decision
            self.last_direction = direction
            return direction
        if self.last_nonStar == self.order[self.orderI - 1] and self.orderI % 2 \
                == 1 and self.order[self.orderI - 1] != 'wait':  # Skips the check of previous path to save steps
            self.orderI += 2
        self.last_direction = self.order[self.orderI - 1]
        return self.order[self.orderI - 1]

    def find_map_tile(self, x, y):
        for i in self.map:
            if i.coordinate[0] == x and i.coordinate[1] == y:
                return i

    def update_position(self):  # updates the current position of the dude
        print "STATE POS: (", self.state_pos[0], ",", self.state_pos[1], ")"
        if self.last_direction == 'up' and self.last_result != 'failure':
            self.state_pos[1] = self.state_pos[1]+1
        elif self.last_direction == 'down' and self.last_result != 'failure':
            self.state_pos[1] = self.state_pos[1]-1
        elif self.last_direction == 'left' and self.last_result != 'failure':
            self.state_pos[0] = self.state_pos[0]-1
        elif self.last_direction == 'right' and self.last_result != 'failure':
            self.state_pos[0] = self.state_pos[0]+1

    def make_map_tile(self):  # checks the tile and adds a new tile if there is not one found
        exist_flag = False
        for i in self.map:
            if i.coordinate[0] == self.state_pos[0] and i.coordinate[1] == self.state_pos[1]:
                exist_flag = True
        if not exist_flag:
            self.map = np.append(self.map, MapTiles(self.state_pos[0], self.state_pos[1]))

    def random_direction(self):
        r = random.randint(1, 4)
        # Update last direction to be the one just selected:
        self.last_direction = self.directions[r]
        return self.directions[r]

    def put_result(self, result):  # updates the position at each frame
        self.last_result = result
        self.update_position()
        if result != 'failure':
            self.make_map_tile()
