#Check for previous direction not working
#Github has the most updated code

import random
import numpy as np
class MapTiles:
    def __init__(self, x, y):
        self.coordinate = [x,y]

        self.minesweepernumber = 0
        self.successDirs = ['up', 'down', 'left', 'right']
        self.successPrio = [3, 3, 3, 3]
        self.priority = 3 #minesweeper number plus priority
class DecisionFactory:
    def __init__(self, name='Dude'):
        self.name = name
        self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
        self.results = [ 'success', 'failure', 'portal' ]
        self.order = ['up','down','right','left','down','up','left','right','wait']
        self.last_result = self.results[0]
        self.last_direction = 'wait'
        self.state_pos = [0, 0]
        self.last_nonStar = 'wait'
        self.map = np.array([])
        self.set_direction = 0;

        #np.append(self.map,MapTiles(self.state_pos[0],self.state_pos[1]))
        self.map = np.append(self.map,MapTiles(0,0))
        self.orderI = 0
        self.prioDirs = ['up','right','down', 'left']

    # Note: we have relativistic coordinates recorded here, since the map
    #   is relative to the player's first known and recorded position:
    # self.state.pos = (0, 0)

    def make_decision(self):
        flag = True
        maxvalue = 0
        dude = 0
        currTile =self.findMapTile(self.state_pos[0],self.state_pos[1])
        for i in range(0,4):
            print("IN THE FOR LOOP")
            if flag:
                maxvalue = currTile.successPrio[i]
                flag = False
            if currTile.successPrio[i] > maxvalue:
                maxvalue = currTile.successPrio[i]
        #print("NUM",  num)
        for i in range(0,4):
            if currTile.successPrio[i] == maxvalue:
                dude = i
                break
        currTile.successPrio[dude] -= 1
        print("MAXVALUE1", maxvalue)
        print("PRIO ARRAY", currTile.successPrio)
        #print("BOOM2", currTile.successPrio[num])
        self.update_priority(currTile.successDirs[dude])
        print currTile.successDirs[dude]
        #self.lastCoordinate = [self.state_pos[0], self.state_pos[1]]
        self.last_nonStar = currTile.successDirs[dude]
        if currTile.successDirs[dude] == 'up':
            self.last_nonStar = 'down'
        elif currTile.successDirs[dude] == 'down':
            self.last_nonStar = 'up'
        elif currTile.successDirs[dude] == 'left':
            self.last_nonStar = 'right'
        elif currTile.successDirs[dude] == 'right':
            self.last_nonStar = 'left'
        return currTile.successDirs[dude]

    def update_priority(self, direction):
        local_dudex = self.state_pos[0]
        local_dudey = self.state_pos[1]
        oppDirection = ''
        if direction == 'up':
            local_dudey = self.state_pos[1]+1
            oppDirection = 'down'
        elif direction == 'down':
            local_dudey = self.state_pos[1]-1
            oppDirection = 'up'
        elif direction == 'left':
            local_dudex = self.state_pos[0]-1
            oppDirection = 'right'
        elif direction == 'right':
            local_dudex = self.state_pos[0]+1
            oppDirection = 'left'
        currTile =self.findMapTile(local_dudex, local_dudey)
        print("Curtile", currTile)
        print("POS", self.state_pos[0], self.state_pos[1])
        for i in range(0, 4):
            if currTile.successDirs[i] == oppDirection:
                currTile.successPrio[i] -= 1
    def get_decision(self, verbose = True):
        print(self.state_pos)
        direction = ''
        currTile =self.findMapTile(self.state_pos[0], self.state_pos[1])
        print("CURTILE", currTile)
        #self.order = ['up','down','right','left','down','up','left','right','wait']
        self.orderI += 1
        if self.last_result == 'failure':
            self.orderI -= 1
            for i in range(0, 4):
                if self.order[self.orderI - 1] == currTile.successDirs[i]:
                    currTile.successDirs[i] = "Dan"
                    currTile.successPrio[i] = -999
            self.orderI += 2
        if self.orderI >= 10:
            self.orderI = 0
            direction = self.make_decision()
            self.last_direction = direction
            return direction
        #print("OI", self.orderI)
        if self.last_nonStar == self.order[self.orderI - 1] and self.orderI % 2 == 1 and self.order[self.orderI - 1] != 'wait':
            self.orderI += 2
        self.last_direction = self.order[self.orderI - 1]
        return self.order[self.orderI - 1]







        '''print(self.state_pos)
        local_dudex = self.state_pos[0]
        local_dudey = self.state_pos[1]
        self.orderI += 1
        if self.orderI >= 9:
            self.orderI = 0
            next_dir = self.make_decision();
            return next_dir
        print("OGRE" , self.orderI)
        if self.order[self.orderI - 1] == 'up':
            local_dudey = self.state_pos[1]+1
        elif self.order[self.orderI - 1] == 'down':
            local_dudey = self.state_pos[1]-1
        elif self.order[self.orderI - 1] == 'left':
            local_dudex = self.state_pos[0]-1
        elif self.order[self.orderI - 1] == 'right':
            local_dudex = self.state_pos[0]+1
        print("GARBAGE" ,self.lastCoordinate[0], self.lastCoordinate[1], local_dudex, local_dudey, self.orderI % 2);

        #if self.orderI % 2 == 1 and self.lastCoordinate[0] == local_dudex and self.lastCoordinate[1] == local_dudey:
        #    print("How the hell are we here")
        #    self.orderI += 1
        if self.last_result == 'failure':
            self.orderI += 1
            currTile = self.findMapTile(self.state_pos[0],self.state_pos[1])
            currTile.minesweepernumber += 1
            print("MinesweeperNumber", currTile.minesweepernumber)
        if self.set_direction == 2:
            possible_direction = ''
            if self.last_direction == 'up':
                print("IN UP")
                possible_direction = 'down'
            elif self.last_direction == 'down':
                print("IN DOWN")
                possible_direction = 'up'
            elif self.last_direction == 'left':
                print("IN LEFT")
                possible_direction = 'right'
            elif self.last_direction == 'right':
                print("IN RIGHT")
                possible_direction = 'left'

            currTile = self.findMapTile(self.state_pos[0],self.state_pos[1])
            #print(" DIRECTION " , possible_direction)
            #print(" PRIO " , currTile.priority)
            #print(" X " , currTile.coordinate)
            if self.last_direction != 'wait':
                currTile.successDirs.append(possible_direction)
            currTile.successPrio.append(currTile.priority)
            self.set_direction = 1
        elif self.last_result == 'success':
            self.set_direction += 1
        print("FINAL ORDER I" , self.orderI, self.last_direction)
        self.last_direction = self.order[self.orderI-1]
        #print("FINAL ORDER I" , self.orderI)
        return self.order[self.orderI-1]
'''
    def next_direction(self):
        prioDir = self.results[4]
        self.get_decision(self)
        #self.update_position()
       # self.map.append(MapTiles(self.state_pos[0],self.state_pos[1]))
        #when picking a decision, check array if in there, if it is then pick a new one
        #store the failed decision so we don't pick it again

    def findMapTile(self,x,y):
        for i in self.map:
            #print ("Here", i)
            if i.coordinate[0] == x and i.coordinate[1] == y:
                return i
        #self.make_MapTile()

    def update_position(self):
        print("IN UPDATE POSITION")
        print("LAST RESULT ", self.last_result)
        print("LAST DIRECTION", self.last_direction)
        if self.last_direction == 'up' and self.last_result != 'failure':
            self.state_pos[1] = self.state_pos[1]+1
        elif self.last_direction == 'down' and self.last_result != 'failure':
            self.state_pos[1] = self.state_pos[1]-1
        elif self.last_direction == 'left' and self.last_result != 'failure':
            self.state_pos[0] = self.state_pos[0]-1
        elif self.last_direction == 'right' and self.last_result != 'failure':
            self.state_pos[0] = self.state_pos[0]+1
        print("STATE POS" , self.state_pos[0], self.state_pos[1])
    def make_MapTile(self):
        existFlag = False
        #print("LAST RESULT ", self.last_result)
        #print("STATE POS", self.state_pos[0], self.state_pos[1])
        for i in self.map:
            print("MAP" , i.coordinate[0], i.coordinate[1])
            if i.coordinate[0] == self.state_pos[0] and i.coordinate[1] == self.state_pos[1]:
                existFlag = True
        if not existFlag:
            #print ("STATE POS", self.state_pos[0], self.state_pos[1])
            self.map = np.append(self.map, MapTiles(self.state_pos[0],self.state_pos[1]))


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