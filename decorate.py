from tkinter import *
import pygame as pyg
import game
from fractions import *

class GUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("Start")
        self.win.geometry("250x200")

        self.random_se = BooleanVar()

    def gen_map(self):
        try:
            size = int(self.entry1.get())
            if(size % 2 == 0 or size <= 3):
                raise ValueError

            if(self.entry2.get() != ""):
                disj_st = float(Fraction(self.entry2.get()))
            else:
                disj_st = 2.0

            if(self.entry3.get() != ""):
                rect_st = float(Fraction(self.entry3.get()))
            else:
                rect_st = 1/6
        except ValueError:
                self.win2 = Tk()
                self.win2.geometry("50x50")
                msg = Message(self.win2, text="Invalid")
                msg.pack(side=LEFT)
                return -1
        else:
            print(size, disj_st, rect_st)
            #print(self.random_se.get())
            game.play(size, disj_st, rect_st, self.random_se.get())

    def Create(self):
        self.label1 = Label(self.win, text="Size(odd int| n>3): ")
        self.label1.pack()
        self.entry1 = Entry(self.win)
        self.entry1.pack()

        self.label2 = Label(self.win, text="Disjoint Strength(rat| st>=0): ")
        self.label2.pack()
        self.entry2 = Entry(self.win)
        self.entry2.pack()

        self.label3 = Label(self.win, text="Rectgen Strength(rat| st>=0): ")
        self.label3.pack()
        self.entry3 = Entry(self.win)
        self.entry3.pack()

        check1 = Checkbutton(self.win, text="Random start and end", variable=self.random_se,
                             offvalue=False, onvalue=True)
        check1.pack()

        button1 = Button(self.win, text="Generate!", command=self.gen_map)
        button1.pack()

        self.win.mainloop()


def main():
    insta1 = GUI()
    insta1.Create()

if __name__ == '__main__':
    main()