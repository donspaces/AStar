import numpy as np
import game
import time

def gen_map(size, disj_st, rect_st):
    a = np.zeros([size, size], dtype=int)

    Open_Set = set() #Set of points going to be processed
    Close_Set = set() #Set of points visited

    def StartMap():
        '''
        Generate the initial crosses map with 4 walls on each middle block.
        '''
        for i in range(size):
            for j in range(size):
                if(i % 2 == 0):
                    a[i, j] = 1
                else:
                    if(j % 2 == 0):
                        a[i, j] = 1

    def disjoint(st):
        '''
        :param st: optimization strength (st > 0) (float)
        A map with random disjoint points.
        '''
        if(size < 11):
            return

        randn = [0] * (int(size * st * 2))
        for i in range(int(size * st)):
            randn[i * 2] = np.random.randint(1, size - 1)
            randn[i * 2 + 1] = np.random.randint(1, size // 2) * 2

        coords = []
        for i in range(int(size * st)):
            coords.append((randn[i * 2], randn[i * 2 + 1]))
        print(coords)

        for i in coords:
            a[i] = 0


    def initial():
        '''
        :return coordinate of initial point x, y
        Set a random initial point on the edge of the map.
        '''
        init = np.random.randint(0, 4)
        select = {
            0: (1, np.random.randint(0, size // 2) * 2 + 1), #top
            1: (size - 2, np.random.randint(0, size // 2) * 2 + 1),
            2: (np.random.randint(0, size // 2) * 2 + 1, 1), #left
            3: (np.random.randint(0, size // 2) * 2 + 1, size - 2),
        }

        x, y = select[init]

        return x, y

    def rect_gen(st, maxima = size // 10):
        '''
        :param st: generation strength (st in rational and st >= 0) (float)
        :param maxima: max rectangle size
        Append random rectangles in map.
        '''
        if(size < 31 or st == 0 or maxima < 3):
            return

        rand_param = {'cord': [], 'size': []}
        for i in range(int(size // (1 / st))):
            rand_param['size'].append(tuple(np.random.randint(1, maxima // 2 + 1, size=2) * 2 + 1))
            randa = np.random.randint(rand_param['size'][i][0] // 2, size // 2 - 1) * 2 + 1
            randb = np.random.randint(rand_param['size'][i][1] // 2, size // 2 - 1) * 2 + 1
            rand_param['cord'].append((randa, randb))

        print(rand_param)

        for i in range(len(rand_param['cord'])):
            cord = rand_param['cord'][i]
            rect = rand_param['size'][i]
            for j in range(cord[0] - rect[0] + 1, cord[0] + 1):
                for k in range(cord[1] - rect[1] + 1, cord[1] + 1):
                    a[j, k] = 0

    def gen(x, y):
        '''
        :param (x, y): initial coordinate
        :return: a set of "ground" points
        Map generation using random prim
        '''
        flag = 0
        #Initial coord
        coord = (x, y)
        #The beginning place
        Close_Set.update({coord})
        #vector functions
        up = lambda cord: (cord[0] - 1, cord[1])
        down = lambda cord: (cord[0] + 1, cord[1])
        left = lambda cord: (cord[0], cord[1] - 1)
        right = lambda cord: (cord[0], cord[1] + 1)
        #Iterate through random points on path
        while(len(Open_Set) != 0 or flag == 0):
            flag = 1

            for i in [up(coord), down(coord), left(coord), right(coord)]:
                if (i[0] < size - 1 and i[1] < size - 1 and i[0] > 0 and i[1] > 0 and a[i] == 1):
                    if(i not in Close_Set and i not in Open_Set):
                        Open_Set.update({i}) #Update if not in Close_Set(Unvisited) and Open_Set

            next = None
            while next == None:
                if(Open_Set == set()):
                    break
                # In this part we are gonna select a random point(wall) in the Open_Set

                # If the point(wall) is in between two separate walls, one visited and
                # one unvisited, then push the wall down and mark it as visited.

                # If the point(wall) is in between two separate walls, both visited
                # ,then remain the wall and delete it from Open_Set.
                sel_list = list(Open_Set)
                sel = np.random.randint(0, len(sel_list))

                wall = sel_list[sel]
                bar = 0
                bar2 = 0
                for i in [up(wall), down(wall)]:
                    if(a[i] == 0):
                        if(i in Close_Set):
                            bar += 1
                        if(i not in Close_Set):
                            next = i

                for i in [left(wall), right(wall)]:
                    if(a[i] == 0):
                        if(i in Close_Set):
                            bar2 += 1
                        if(i not in Close_Set):
                            next = i

                if(bar == 0 and bar2 == 0):
                    Open_Set.remove(wall)

                if(bar == 1 or bar2 == 1):
                    a[wall] = 0
                    Open_Set.remove(wall)
                    Close_Set.update({wall})
                    Close_Set.update({next})
                elif(bar == 2 or bar2 == 2):
                    Open_Set.remove(wall)

            coord = next

        return Close_Set

    StartMap()
    x, y = initial()
    print(x, y)
    start_t = time.time()
    path = gen(x, y)
    disjoint(disj_st)
    rect_gen(rect_st)
    end_t = time.time()
    print(a)

    dur = end_t - start_t

    return a, dur

def main():
    gen_map()
    #StartMap()
    #disjoint()
    #rect_gen()

if __name__ == '__main__':
    main()



