import random
import math
import time
import argparse
import numpy as np
import pandas as pd
from tkinter import *

from environment import *

# Global Variables
SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e"}

CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2"}

FONT = ("Verdana", 40, "bold")

parser = argparse.ArgumentParser(description='Player mode for Demo')
parser.add_argument('--mode', default='random',
                    type=str, choices=['random', 'best'])
parser.add_argument('--steps', default=1, type=int)
args = parser.parse_args()


class GameGrid(Frame):
    "Creates the grid for demo and associated functions"
    def __init__(self, player):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.grid_cells = []
        self.init_grid()
        self.game = Game()
        self.matrix = self.game._state
        self.update_grid_cells()
        self.wait_visibility()
        self.after(10, self.make_move)
        self.player = player

    def init_grid(self):
        "Initializes the grid frame"
        background = Frame(self, bg=BACKGROUND_COLOR_GAME,
                           width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY,
                             width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j,
                          padx=GRID_PADDING,
                          pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        "Update the grid cells based on the game's state"
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    new_number = 2**new_number
                    self.grid_cells[i][j].configure(text=str(new_number),
                                                    bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def make_move(self):
        "Select action and update the grid"
        done = True
        if len(self.game.available_actions()) == 0:
            done = False
        else:
            move = self.player.select_action(self.game._state)
            self.matrix, reward, game_over, _ = self.game.do_action(move)
        if game_over is True:
            self.master.title('2048 Score {}'.format(self.game.score()))
            self.grid_cells[1][1].configure(text="You",
                                            bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!",
                                            bg=BACKGROUND_COLOR_CELL_EMPTY)
            done = False
            return
        self.update_grid_cells()
        if done is True:
            self.after(30, self.make_move)


def main():
    "Main function"
    if args.mode == 'best':
        player = MultiStepPlayer(args.steps)
    else:
        player = RandomPlayer()
    root = Tk()
    gamegrid = GameGrid(player)
    root.mainloop()


if __name__ == '__main__':
    main()