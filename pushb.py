from queue import *
import numpy as np
import scipy as sp
import math
from matplotlib import pyplot
import time
import pygame as pyg
import generator as gen
import game
import sys
import time

def push_algo(size, disj_st, rect_st, rand_se):

    Open_set = set()
    Close_set = set()


    grid = np.zeros([size, size])


    def distance(a, b):
        return (abs(b[1]-a[1])+abs(b[0]-a[0])) * 10

    class A_block:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.parent = None
            self.g = 0
            self.h = 0
            self.f = 0
            self.type = 0

        def __str__(self):
            f = self.f
            g = self.g
            h = self.h
            stri = "(" + str(self.x) + ", " + str(self.y) + ") :"
            stri += " (" + str(f) + ", " + str(g) + ", " + str(h) + ")"

            return stri

    def randomStartEnd():
        '''
        A function generating random starting and ending points
        '''
        rand1 = np.random.randint(0, size // 4, size=2) * 2 + 1
        rand2 = np.random.randint(size // 4, size // 2, size=2) * 2 + 1

        start = (rand1[0], rand1[1])
        end = (rand2[0], rand2[1])

        return start, end

    def init_A_matrix(grid):
        '''
        :param grid: initialize the matrix according to the map grid.
        :return: the A_matrix
        A_matrix is a ndarray with type of A_block in order to save infos
        '''
        matrix = np.ndarray([size, size], dtype=A_block)
        for i in range(size):
            for j in range(size):
                matrix[i, j] = A_block(i, j)
                matrix[i, j].type = grid[i, j]

        return matrix

    def A_star(coord, end, A_matrix):
        '''
        :param coord: recent coordinate of the player
        :param end: ending point
        :param A_matrix: A_block matrix
        :return: The coordinate of the current player
        A_star algorithm.
        '''
        while(coord != end):
            #dir vectors
            up = (coord[0] - 1, coord[1])
            down = (coord[0] + 1, coord[1])
            left = (coord[0], coord[1] - 1)
            right = (coord[0], coord[1] + 1)

            mini = -1
            next_coord = None

            for i in [up, down, left, right]:
                if(i[0] < size and i[1] < size and i[0] > 0 and i[1] > 0):
                    if (A_matrix[i] not in Close_set and A_matrix[i] not in Open_set and
                            (A_matrix[i].type == 0 or A_matrix[i].type == 2)):
                        #The point for processing must be valid, unvisited and not in Open_Set
                        A_matrix[i].g = A_matrix[coord].g + 10
                        A_matrix[i].h = distance(i, end)
                        A_matrix[i].f = A_matrix[i].g + A_matrix[i].h
                        A_matrix[i].parent = A_matrix[coord]
                        Open_set.update({A_matrix[i]})

            #print([str(i) for i in Open_set])

            if(Open_set == set()):
                raise(Exception("No pathway found!"))
                return -1

            for block in Open_set:
                if mini == -1 or block.f < mini:
                    mini = block.f #Finding the smallest f
                    next_coord = (block.x, block.y)

            #print(next_coord)
            next = A_matrix[next_coord]
            Open_set.remove(next)
            Close_set.update({next})
            coord = next_coord

        return coord

    def find_path(begin, last, A_matrix):
        '''
        :param begin: tuple[int, int]
        :param last: ~
        :param A_matrix: A_block matrix
        :return: The path which had been found
        Retrieve the path.
        '''
        coord = last
        pathw = []
        while coord != begin:
            # Iterating through parents of nodes from end to start
            pathw.append(coord)
            par = A_matrix[coord].parent
            coord = (par.x, par.y)

        return pathw

    def paint_grid(start, end, pusher=(0, 0)):
        for i in range(2, 8):
            for j in range(5, 7):
                grid[i, j] = 1

        grid[start] = -1
        grid[end] = 2

        return grid


    if(rand_se):
        start, end = randomStartEnd()
    else:
        start = (1, 1)
        end = (size - 2, size - 2)

    pusher = (5, 3)
    grid, dur_g = gen.gen_map(size, disj_st, rect_st)
    grid[start] = -1
    grid[end] = 2
    print(grid)

    A_matrix = init_A_matrix(grid)
    try:
        start_t = time.time()
        co = A_star(start, end, A_matrix)
        end_t = time.time()
    except Exception as ex:
        print(ex.args[0])
        sys.exit()
    else:
        pathw = find_path(start, end, A_matrix)
        pathw.reverse()
        pathw.insert(0, start)
        print(pathw)

        pathww = pathw.copy()
        pathww.pop()

        gridl = grid.copy()
        for i in pathww:
            gridl[i] = -1

        print(gridl)

        dur_p = end_t - start_t

        return pathw, grid, gridl, dur_p, dur_g


if __name__ == '__main__':
    push_algo()

