
import curses
import time
import random

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

pieces = {
        'I' : [
            [Point(-2,0), Point(-1,0), Point(0,0), Point(1, 0)],
            [Point(0,-2), Point(0, -1), Point(0,0), Point(0, 1)],
            [Point(-2,0), Point(-1,0), Point(0,0), Point(1, 0)],
            [Point(0,-2), Point(0, -1), Point(0,0), Point(0, 1)]
        ],
        'J' : [
            [Point(1,0), Point(0,0), Point(-1,0), Point(-1, -1)],
            [Point(0,1), Point(0,0), Point(0,-1), Point(1, -1)],
            [Point(-1,0), Point(0,0), Point(1,0), Point(1, 1)],
            [Point(0,-1), Point(0,0), Point(0,1), Point(-1, 1)]
        ],
        'L' : [Point(-1,1), Point(-1,0), Point(0,0), Point(1, 0)],
    }

colors = {
    'I' : 1,
    'J' : 2
}

class Tetris:
    def __init__(self):
        self.board = [[0 for x in range(10)] for y in range(20)]

    def checkPos(self, newPos, newRot):
        for p in pieces[self.piece][newRot]:
            x = newPos.x + p.x
            y = newPos.y + p.y
            if x < 0 or x > 9 or y > 19 or self.board[y][x] != 0:
                return False
        return True

    def checkX(self, dx):
        newPos = Point(self.pos.x + dx, self.pos.y)
        return newPos if self.checkPos(newPos, self.rotation) else self.pos

    def checkRot(self, dr):
        newRot = (self.rotation + dr) % 4
        return newRot if self.checkPos(self.pos, newRot) else self.rotation

    def checkDown(self):
        newPos = Point(self.pos.x, self.pos.y + 1)
        return self.checkPos(newPos, self.rotation)

    def lockPiece(self):
        for p in pieces[self.piece][self.rotation]:
            x = self.pos.x + p.x
            y = self.pos.y + p.y
            self.board[y][x] = colors[self.piece]
        self.redrawBoard()
        self.choosePiece()

    def redrawBoard(self):
        self.playArea.attrset(curses.color_pair(0))
        self.playArea.border()
        for y in range(20):
            for x in range(10):
                if self.board[y][x] > 0:
                    self.playArea.attrset(curses.color_pair(self.board[y][x]))
                    self.playArea.addstr(y + 1, (x*2) + 1 , "  ")

        self.playArea.refresh()
        pass

    def drawPiece(self, color):
        self.playArea.attrset(curses.color_pair(color))
        for p in pieces[self.piece][self.rotation]:
            if p.y + self.pos.y > 0:
                self.playArea.addstr(p.y + self.pos.y + 1, (p.x + self.pos.x)*2 + 1 , "  ")

    def choosePiece(self):
        self.piece = random.choice(['I', 'J'])
        self.rotation = 0
        self.pos = Point(5,0)

    def loop(self):
        # Draw the piece
        self.drawPiece(colors[self.piece])

        self.playArea.refresh()

        # then erase for next frame
        self.drawPiece(0)

        ch = self.stdscr.getch()
        if ch == ord('q') or ch == ord('Q'): return False
        elif ch == curses.KEY_RIGHT: self.pos = self.checkX(1)
        elif ch == curses.KEY_LEFT: self.pos = self.checkX(-1)
        elif ch == curses.KEY_UP: self.rotation = self.checkRot(1)
        elif ch == curses.KEY_DOWN and self.checkDown(): self.pos = Point(self.pos.x, self.pos.y + 1)

        now = time.time()
        self.acc += now - self.then
        if self.acc > 1:
            self.acc = 0
            if self.checkDown():
                self.pos = Point(self.pos.x, self.pos.y + 1)
            else:
                self.lockPiece()
        self.then = now
        return True

    def run(self, stdscr):

        self.stdscr = stdscr

        if curses.has_colors():
            fg = curses.COLOR_WHITE
            curses.init_pair(1, fg, curses.COLOR_RED)
            curses.init_pair(2, fg, curses.COLOR_CYAN)

        curses.nl()
        curses.noecho()
        curses.curs_set(0)

        stdscr.timeout(0)

        if curses.COLS < 40 or curses.LINES < 20:
            raise Exception("Need a bigger console")

        stdscr.refresh()
        self.playArea = curses.newwin(22, 22, (curses.LINES - 22) // 2, 1)
        self.playArea.border()
        self.playArea.refresh()

        self.choosePiece()
        self.then = time.time()
        self.acc = 0.0
        while self.loop():
            pass

t = Tetris()
curses.wrapper(t.run)