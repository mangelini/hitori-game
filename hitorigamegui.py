#!/usr/bin/env python3

"""
    Hitori Project
    Not working: 10.8
    Semi-working: backtracking works with 5x5, 6x6, 9x9, 15x15 boards, not with 8x8 and 12x12 (maybe too complex).
"""

import g2d
from hitori_game import HitoriGame
from time import time
from sys import exit
from os import name, system

W, H = 40, 40
LONG_PRESS = 0.5
solved = False

class HitoriGameGui:
    def __init__(self, g: HitoriGame):
        self._game = g
        self._downtime = 0
        self.update_buttons()

    def tick(self):
        global solved

        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._downtime > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
            self.update_buttons()
        if g2d.key_pressed("a"):
            self._game.mark_auto()
        elif g2d.key_released("a"):
            self.update_buttons()
        if g2d.key_pressed("h"):
            self._game.user_helper()
        elif g2d.key_released("h"): 
            self.update_buttons()
        if g2d.key_pressed("r"):
            if not solved:
                while not solved:
                    solved = self._game.solve_recursive(0)
            else:
                solved = False
                self._game.clear_board()
        elif g2d.key_released("r"): 
            self.update_buttons()

    def update_buttons(self):
        global solved

        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y)
                
                if '#' not in value:
                    center = x * W + W//2, y * H + H//2

                    if '!' in value:
                        g2d.set_color((0, 0, 200))
                        g2d.fill_circle(center, 14)
                        g2d.set_color((255, 255, 255))
                        g2d.fill_circle(center,12)
                        g2d.set_color((0, 0, 0))
                    g2d.draw_text_centered(value[:-1], center, H//2)
                else:
                    g2d.fill_rect((x * W, y * H, W, H))
        g2d.update_canvas()

        if self._game.finished() and not solved:
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: HitoriGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = HitoriGameGui(game)
    g2d.main_loop(ui.tick)


def clrscr():
    # Clear screen for windows and linux/mac
    if name == 'nt': 
        _ = system('cls')
    else: 
        _ = system('clear')

def cli_setup():
    choice = 0

    while choice != 2:
        choice = int(input(
                'Insert:\n'
                '1 -> to view the manual\n'
                '2 -> to start the game\n'
                '3 -> Exit\n'))
        
        if choice == 1:
            clrscr() # Clear screen

            with open('manual.txt', 'r') as f:
                man = f.read()
            print(man)

            input('\nPress Enter to return to the menu\n')
        
        if choice == 2:
            clrscr() # Clear screen
            
            difficulty = int(input(
                'Insert difficulty: \n'
                '1 -> Easy 5x5\n'
                '2 -> Medium 6x6\n'
                '3 -> Hard 8x8\n'
                '4 -> Very hard 9x9\n'
                '5 -> Super hard 12x12\n'
                '6 -> Impossible 15x15\n'   
            ))

            if difficulty == 1:
                gui_play(HitoriGame('hitori-5x5-15266.txt'))
            elif difficulty == 2:
                gui_play(HitoriGame('hitori-6x6-16075.txt'))
            elif difficulty == 3:
                #gui_play(HitoriGame('hitori-8x8-21330.txt'))
                gui_play(HitoriGame('init_values.csv'))
            elif difficulty == 4:
                gui_play(HitoriGame('hitori-9x9-168142.txt'))
            elif difficulty == 5:
                gui_play(HitoriGame('hitori-12x12-29512.txt'))
            elif difficulty == 6:
                gui_play(HitoriGame('hitori-15x15-2564.txt'))
        
        if choice == 3:
            exit()
        
        clrscr() # Clear screen

cli_setup()