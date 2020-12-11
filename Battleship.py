import pygame as py
import numpy as np
import math
import pyevolve as pyevol
import random
import copy
import importlib

#from Map import print_board, set_board


POP_SIZE = 10
GENERATIONS = 100
board = np.full((10, 10), 0)


class Tiles:

    def __init__(self, x, y):
        self.coordinate = [x, y]
class Gamer:

    def __init__(self, fitness_val = 0):
        self.fitness_val = fitness_val
        self.hits = np.array([])
        counter = 0
        while True:
            #print(counter)
            in_hits = False
            x_cord = random.randint(0, 9)
            y_cord = random.randint(0, 9)
            #print"xcord: " + str(x_cord) +" " + "ycord: " + str(y_cord),
            #print
            temp_Tile = Tiles(x_cord, y_cord)
            in_hits = check_dup(self, x_cord, y_cord)
            if in_hits is False:
                self.hits = np.append(self.hits, temp_Tile)
                counter +=1
            if counter == 17:
                break
        calc_fitness(self)
    def print_hits(self):
        for i in range(0, len(self.hits)):
            print "(" + str(self.hits[i].coordinate[0]) + "," + (str(self.hits[i].coordinate[1])) + ")",
        print str(self.fitness_val)
def calc_fitness(Gamer):

    Gamer.fitness_val = 0
    for i in range(0, 17):
        if board[Gamer.hits[i].coordinate[0]][Gamer.hits[i].coordinate[1]] != 0:
            Gamer.fitness_val +=1

def most_fit(gamers):
    best_gamer = 0
    temp = gamers[0].fitness_val
    for i in range(0, len(gamers)):
        if gamers[i].fitness_val > temp:
            temp = gamers[i].fitness_val
            best_gamer = i
    return best_gamer
def check_dup(gamer, x_cord, y_cord):
    in_hits = False
    for i in range(0, len(gamer.hits)):
        if gamer.hits[i].coordinate[0] is x_cord and gamer.hits[i].coordinate[1] is y_cord:
            in_hits = True
    return in_hits


def mutation_func(gamer):
    is_dup = True
    lower_fit = True
    if gamer.fitness_val == 17:
        return is_dup
    while is_dup:
        direction = random.randint(0, 1)
        cord = random.randint(0, 16)
        temp = random.random()

        if temp < 0.5:
            temp = 1
        else:
            temp = -1

        x_cord = gamer.hits[cord].coordinate[0]
        y_cord = gamer.hits[cord].coordinate[1]
        temp_x = gamer.hits[cord].coordinate[0]
        temp_y = gamer.hits[cord].coordinate[1]
        if direction == 0:
            x_cord += temp
        elif direction == 1:
            y_cord += temp
        #print (str(direction) + " " + str(cord) + " " +str(temp))

        if x_cord == 10:
            x_cord = 0
        if x_cord == -1:
            x_cord = 9
        if y_cord == 10:
            y_cord = 0
        if y_cord == -1:
            y_cord = 9
        is_dup = check_dup(gamer, x_cord, y_cord)

    gamer.hits[cord].coordinate[0] = x_cord
    gamer.hits[cord].coordinate[1] = y_cord
    fitness = gamer.fitness_val
    calc_fitness(gamer)

    if gamer.fitness_val < fitness:
        lower_fit = False
        gamer.hits[cord].coordinate[0] = temp_x
        gamer.hits[cord].coordinate[1] = temp_y
        gamer.fitness_val = fitness
    return lower_fit

def set_board():
    orientation = random.randint(0, 1)
    dist_ships = 3
    ship_size = [5, 4, 3, 3, 2 ]

    for i in range(0, len(ship_size)):
        orientation = random.randint(0, 1)
        #Horizontal
        if orientation == 0:
            while True:
                cleared = True
                ship_row = random.randint(0, 9)
                ship_col = random.randint(0, 9 - ship_size[i])
                #print(str(orientation) + str(ship_row) + str(ship_col))
                for j in range(ship_col, ship_col + ship_size[i]):
                    if board[ship_row][j] != 0:
                        cleared = False
                if cleared:
                    break
            for j in range(ship_col, ship_col + ship_size[i]):
                if ship_size[i] == 3:
                    board[ship_row][j] = dist_ships
                else:
                    board[ship_row][j] = ship_size[i]
            if ship_size[i] == 3:
                dist_ships = 1
        #Vertical
        if orientation == 1:
            while True:
                cleared = True
                ship_row = random.randint(0, 9 - ship_size[i])
                ship_col = random.randint(0, 9)
                #print(str(orientation) + str(ship_row) + str(ship_col))
                for j in range(ship_row, ship_row + ship_size[i]):
                    if board[j][ship_col] != 0:
                        cleared = False
                if cleared:
                    break
            for j in range(ship_row, ship_row + ship_size[i]):
                #print (dist_ships)
                if ship_size[i] == 3:
                    board[j][ship_col] = dist_ships
                else:
                    board[j][ship_col] = ship_size[i]
            if ship_size[i] == 3:
                dist_ships = 1
    print (board)
def get_board():
    return board

def init_gamers():
    temp_gamer = Gamer()
    gamers = []
    for i in range(0, POP_SIZE):
        gamers.append(temp_gamer)
        temp_gamer = Gamer()
    return gamers

def print_gamers(gamers):
    for i in range(0, POP_SIZE):
        gamers[i].print_hits()
    print

def do_gen(gamers):
    mutate_gamers = []
    #call a function to call the mutator
    #The function makes sure there is improvement
    temp = most_fit(gamers)
    for i in range(0, POP_SIZE):
        mutate_gamers.append(copy.deepcopy(gamers[i]))
    for k in range(0, POP_SIZE):
        while True:
            is_mutated = mutation_func(mutate_gamers[k])
            if not is_mutated:
                #add_threshold
                is_mutated = mutation_func(mutate_gamers[k])
            else:
                break
    gamers = mutate_gamers
    mutate_gamers = []
    return gamers
def check_first(gamers):

    for i in range(0,POP_SIZE):
        if gamers[i].fitness_val == 17:
            return True
    return False
def check_all(gamers):

    for i in range(0,POP_SIZE):
        if gamers[i].fitness_val != 17:
            return False
    return True

