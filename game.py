from pygame import *
import pygame
import pushb
import sys
import generator as gen


def play(block_s, disj_st, rect_st, rand_se):

    white = (255, 255, 255)
    green = (0, 255, 0)
    yellow = (167, 167, 0)
    black = (0, 0, 0)
    gray = (100, 100, 100)
    red = (255, 0, 0)
    light_blue = (173, 216, 230)

    size = (700, 700)

    #block_s = pushb.size
    #block_s = gen.size

    unit = size[1] / (block_s + 1)

    def draw_grid(screen):
        '''
        Drawing grids
        '''
        for i in range(1, block_s + 1):
            y_pos = unit * i
            draw.line(screen, gray, (0, y_pos), (size[0], y_pos), width=1)

            x_pos = unit * i
            draw.line(screen, gray, (x_pos, 0), (x_pos, size[1]), width=1)



    def draw_text(screen):
        '''
        Labeling each rows and cols
        '''
        screen.get_rect()

        font1 = font.SysFont("Times New Roman", int(600 / block_s))

        for i in range(block_s):
            surf1 = font1.render(str(i), True, black)
            screen.blit(surf1, (unit * (i + 1), 0))

            surf2 = font1.render(str(i), True, black)
            screen.blit(surf2, (0, unit * (i + 1)))


    def draw_rect(screen):
        rect1 = Rect((0, 0), (unit, unit))
        draw.rect(screen, black, rect1)

        return rect1

    def apply_grid(screen, grid):
        '''
        Project the ndarray grid onto the screen
        '''
        color_map = {-1: red, 1: gray, 2: green}

        for i in range(block_s):
            for j in range(block_s):
                if(grid[i, j] != 0):
                    rect_b = Rect((unit * (j + 1) + 1, unit * (i + 1) + 1), (unit, unit))
                    draw.rect(screen, color_map[grid[i, j]], rect_b)
                    if(grid[i, j] == -1):
                        pos = (unit * (j + 1.5) + 1, unit * (i + 1.5) + 1)


    def draw_actor(screen, pos):
        '''
        Draw actor
        '''
        cir = draw.circle(screen, gray, pos, radius=(0.4) * unit)

        return cir

    def draw_path(screen, term, pushw):
        '''
        Draw path
        '''
        for i in range(term + 1, len(pushw) - 1):
            rect = Rect(((pushw[i][1] + 1) * unit, (pushw[i][0] + 1) * unit), (unit, unit))
            draw.rect(screen, light_blue, rect)

    def disp_dur(screen, dur_g, dur_p):

        screen.get_rect()
        font1 = font.SysFont("Courier New", 10)

        str1 = "MapGen(prim):" + str(dur_g) + " s."
        text1 = font1.render(str1, True, black)

        str2 = "Search(A*):" + str(dur_p) + " s."
        text2 = font1.render(str2, True, black)

        screen.blit(text1, (unit, 650))
        screen.blit(text2, (unit, 675))

    class Mono:
        def __init__(self):
            init()
            self.screen = display.set_mode(size)
            display.set_caption("pushbox")
            icon = image.load("assets/icon.png")
            display.set_icon(icon)

            self.clock = time.Clock()
            self.pushw, self.grid, self.gridl, self.dur_p, self.dur_g \
                = pushb.push_algo(block_s, disj_st, rect_st, rand_se)
            # grid = gen.gen_map()

        def OnCreate(self):
            pass

        def execute(self):
            self.OnCreate()
            self.TickEvent()
            self.OnDestroy()

        def TickEvent(self):
            term = 0
            QuitMsg = False
            while QuitMsg != True:
                for ev in event.get():
                    if ev.type == QUIT:
                        QuitMsg = True
                        self.OnDestroy()

                self.screen.fill(yellow)

                draw_grid(self.screen)
                draw_text(self.screen)
                draw_rect(self.screen)
                apply_grid(self.screen, self.grid)

                cir = draw_actor(self.screen, ((self.pushw[term][1] + 1.5) * unit, (self.pushw[term][0] + 1.5) * unit))

                draw_path(self.screen, term, self.pushw)

                disp_dur(self.screen, self.dur_g, self.dur_p)

                if (term < len(self.pushw) - 1):
                    term += 1

                display.flip()
                self.clock.tick(10)

        def OnDestroy(self):
            quit()
            sys.exit()

    win1 = Mono()
    win1.OnCreate()
    win1.execute()


if __name__ == '__main__':
    play()