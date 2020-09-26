import random
import numpy as np
class MapTiles:
    def __init__(self, x, y):
        self.coordinate = [x,y]
        self.minesweepernumber = 0
        self.successDirs = []
        self.checkedSuccessDirs = []
        self.priority = 1 #minesweeper number plus priority
    '''
    def setSurroundingWalls(self,numofwalls):
        self.minesweepernumber = numofwalls
    '''
class DecisionFactory:
    def __init__(self, name='Dude'):
        self.name = name
        self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
        self.results = [ 'success', 'failure', 'portal' ]
        self.last_result = self.results[0]
        self.last_direction = 'wait'
        self.state_pos = [0, 0]
        self.map = np.array([])
        self.set_direction = False;
        #np.append(self.map,MapTiles(self.state_pos[0],self.state_pos[1]))
        self.map = np.append(self.map ,MapTiles(0,0))
        self.orderI = 0
        self.prioDirs = ['up','right','down']

    # Note: we have relativistic coordinates recorded here, since the map
    #   is relative to the player's first known and recorded position:
    # self.state.pos = (0, 0)


    def get_decision(self, verbose = True):
        print(self.state_pos)
        order = ['up','down','right','left','down','up','left']
        self.orderI += 1
        if self.orderI >= 8:
            self.orderI = 1
        if self.last_result == 'failure':
            self.orderI += 1
            currTile = self.findMapTile(self.state_pos[0],self.state_pos[1])
            #self.update_position()
            currTile.minesweepernumber += 1
            print("MinesweeperNumber", currTile.minesweepernumber)
        if self.set_direction == True :
            possible_direction = ''
            if self.last_direction == 'up' :
                possible_direction = 'down'
            elif self.last_direction == 'down' :
                possible_direction = 'up'
            elif self.last_direction == 'left' :
                possible_direction = 'right'
            elif self.last_direction == 'right' :
                possible_direction = 'left'
            currTile = self.findMapTile(self.state_pos[0],self.state_pos[1])
            currTile.successDirs.append(possible_direction)
            self.set_direction = False
        elif self.last_result == 'success':
            self.set_direction = True
        self.update_position()
        return order[self.orderI-1]

    def next_direction(self):
        prioDir = self.results[4]
        self.get_decision(self)
        self.update_position()
        self.map.append(MapTiles(self.state_pos[0],self.state_pos[1]))
        #when picking a decision, check array if in there, if it is then pick a new one
        #store the failed decision so we don't pick it again

    def findMapTile(self,x,y):
        for i in self.map:
            print ("Here", i)
            if i.coordinate[0] == x and i.coordinate[1] == y:
                return i

    def update_position(self):
        if self.last_direction == 'up' and self.last_result != 'failure':
            print("JESUS CHRIST! 1")
            self.state_pos[1] = self.state_pos[1]+1
        elif self.last_direction == 'down' and self.last_result != 'failure':
            print("JESUS CHRIST! 2")
            self.state_pos[1] = self.state_pos[1]-1
        elif self.last_direction == 'left' and self.last_result != 'failure':
            print("JESUS CHRIST! 3 ")
            self.state_pos[0] = self.state_pos[0]-1
        elif self.last_direction == 'right' and self.last_result != 'failure':
            print("JESUS CHRIST! 4")
            self.state_pos[0] = self.state_pos[0]+1
    def make_MapTile(self):
        existFlag = False
        if self.last_result == 'success':
            for i in self.map:
                if i.coordinate[0] == self.state_pos[0] and i.coordinate[1] == self.state_pos[1]:
                    existFlag = True
            if not existFlag:
                self.map.append(MapTiles(self.state_pos[0],self.state_pos[1]))



    def random_direction(self):
        #r = random.randint(0,4) # Includes wait state
        r = random.randint(1,4) # Does NOT include wait state

        # Update last direction to be the one just selected:
        self.last_direction = self.directions[r]
        return self.directions[r]

    def put_result(self, result):
        self.last_result = result
        self.update_position()
        if result != 'failure':
            self.make_MapTile()