#!/usr/bin/python

import curses
import time
import copy

class Board(object):
    def __init__(self, stdscr):
        curses.curs_set(0)
        #curses.init_pair(curses.COLOR_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(curses.COLOR_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(curses.COLOR_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(curses.COLOR_MAGENTA, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(curses.COLOR_RED, curses.COLOR_BLACK, curses.COLOR_RED)
        b_y = 1
        b_x = 1
        self.height = 20
        self.width = 10
        self.y_limit = self.height - 1
        self.x_limit = self.width - 1

        self.state = []

        for row in range(self.height):
            self.state.append([curses.COLOR_BLACK] * self.width)

        self.old_blocks = copy.deepcopy(self.state)
        self.board = curses.newwin(self.height, self.width * 2, b_y, b_x)

        stdscr.addstr(b_y-1, b_x-1, "                      ", curses.color_pair(curses.COLOR_WHITE))
        for i in range(1, self.height + 1):
            stdscr.addstr(i, 0, " ", curses.color_pair(curses.COLOR_WHITE))
            stdscr.addstr(i, 2, str(i), curses.color_pair(curses.COLOR_WHITE))
            stdscr.addstr(i, (self.width * 2) + 1, " ", curses.color_pair(curses.COLOR_WHITE))
        stdscr.addstr(self.height + 1, 0, "                      ", curses.color_pair(curses.COLOR_WHITE))
        stdscr.refresh()

#    def draw_block(self, y, x, color):
#        self.board.addstr(y, (x*2), "  ", curses.color_pair(color))
#        self.board.refresh()

    def update_blocks(self, color, cords):
        for cord in cords:
            row = cord[0]
            col = cord[1]
            self.state[row][col] = color
        self.draw_board()

    def draw_board(self):
        #self.board.addstr(0, 10, "  ", curses.color_pair(self.state[0][5]))
        for row in range(self.height):
            for col in range(self.width):
                pass
                self.board.insstr(row, col * 2, "  ", curses.color_pair(self.state[row][col]))
        self.board.refresh()


class Piece(object):
    def __init__(self):
        self.x = 5
        self.y = 1
        self.orientation = 0

    def get_cords(self):
        return [(self.y + y, self.x + x) for (y, x) in self.layouts[self.orientation]]

    def get_new_cords(self, y_delta, x_delta):
        return [(y + y_delta, x + x_delta) for (y, x) in self.get_cords()]

    def bounds_valid(self, y_delta, x_delta):
        for cord in self.get_new_cords(y_delta, x_delta):
            row = cord[0]
            col = cord[1]
            if row < 0 or row > self.board.y_limit or col < 0 or col > self.board.x_limit:
                return False
        return True

    def draw(self):
        self.board.update_blocks(self.color, self.get_cords())

    def clear(self):
        self.board.update_blocks(curses.COLOR_BLACK, self.get_cords())

    def rotate(self):
        self.clear()
        self.orientation = (self.orientation + 1) % len(self.layouts)
        self.draw()

    def move(self, y_delta, x_delta):
        if self.bounds_valid(y_delta, x_delta):
            self.clear()
            self.y += y_delta
            self.x += x_delta
            self.draw()

    def move_left(self):
        self.move(0, -1)

    def move_right(self):
        self.move(0, 1)

    def move_down(self):
        self.move(1, 0)

class Piece_T(Piece):
    def __init__(self, board):
        super(Piece_T, self).__init__()
        self.board = board
        self.layouts = [
            [(0, 0), (0, -1), (-1, 0), (0, 1)],
            [(0, 0), (-1, 0), (0, 1), (1, 0)],
            [(0, 0), (0, -1), (0, 1), (1, 0)],
            [(0, 0), (-1, 0), (0, -1), (1, 0)],
        ]
        self.color = curses.COLOR_MAGENTA

def tetris_main(stdscr):
#    stdscr = curses.initscr()
#    curses.noecho()

    b = Board(stdscr)

    p = Piece_T(b)

    p.draw()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_UP:
            p.rotate()
        if c == curses.KEY_DOWN:
            p.move_down()
        if c == curses.KEY_LEFT:
            p.move_left()
        if c == curses.KEY_RIGHT:
            p.move_right()

curses.wrapper(tetris_main)
