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

    def clear_blocks(self, cords):
        for cord in cords:
            row = cord[0]
            col = cord[1]
            self.state[row][col] = curses.COLOR_BLACK
        self.draw_board()

    def update_blocks(self, color, new_cords, old_cords=[]):
        for cord in set(new_cords) - set(old_cords):
            row = cord[0]
            col = cord[1]
            if self.state[row][col] != curses.COLOR_BLACK:
                pass
                return False
        self.clear_blocks(old_cords)
        for cord in new_cords:
            row = cord[0]
            col = cord[1]
            self.state[row][col] = color
        self.draw_board()
        return True

    def draw_board(self):
        #self.board.addstr(0, 10, "  ", curses.color_pair(self.state[0][5]))
        for row in range(self.height):
            for col in range(self.width):
                pass
                self.board.insstr(row, col * 2, "  ", curses.color_pair(self.state[row][col]))
        self.board.refresh()

    def clear_full_rows(self):
        for row in xrange(self.height):
            if curses.COLOR_BLACK not in self.state[row]:
                del self.state[row]
                self.state.insert(0, [curses.COLOR_BLACK] * self.width)
        self.board.refresh()

class Piece(object):
    def __init__(self):
        self.x = 5
        self.y = 1
        self.orientation = 0

    def get_cords(self):
        return [(self.y + y, self.x + x) for (y, x)
                in self.layouts[self.orientation]]

    def get_new_cords(self, y_delta, x_delta, orientation):
        return [(self.y + y + y_delta, self.x + x + x_delta) for (y, x)
                in self.layouts[orientation]]

    def bounds_valid(self, y_delta, x_delta, orientation):
        for cord in self.get_new_cords(y_delta, x_delta, orientation):
            row = cord[0]
            col = cord[1]
            if (row < 0 or row > self.board.y_limit or
                col < 0 or col > self.board.x_limit):
                return False
        return True

    def draw(self, old_cords=[]):
        return self.board.update_blocks(self.color, self.get_cords(), old_cords)

    def rotate(self):
        old_cords = self.get_cords()
        new_orientation = (self.orientation + 1) % len(self.layouts)
        if self.bounds_valid(0, 0, new_orientation):
            self.orientation = new_orientation
            return self.draw(old_cords)
        return False

    def move(self, y_delta, x_delta):
        old_cords = self.get_cords()
        if self.bounds_valid(y_delta, x_delta, self.orientation):
            self.y += y_delta
            self.x += x_delta
            return self.draw(old_cords)
        return False

    def move_left(self):
        return self.move(0, -1)

    def move_right(self):
        return self.move(0, 1)

    def move_down(self):
        return self.move(1, 0)

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

    curses.halfdelay(1)

    t1 = time.time()
    d = 0.5

    while True:
        c = stdscr.getch()
        t2 = time.time()
        if t2 - t1 > d:
            t1 = t2
            if not p.move_down():
                p = Piece_T(b)
        elif c == curses.KEY_DOWN:
            if not p.move_down():
                b.clear_full_rows()
                p = Piece_T(b)
        if c == ord('q'):
            break
        if c == curses.KEY_UP:
            p.rotate()
        if c == curses.KEY_LEFT:
            p.move_left()
        if c == curses.KEY_RIGHT:
            p.move_right()

curses.wrapper(tetris_main)
