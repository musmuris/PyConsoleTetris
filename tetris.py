
import curses
import time

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


class Tetris:
    def __init__(self):
        self.board = [[0] * 10] * 20

    def checkPos(self, newPos, newRot):
        for p in self.piece[newRot]:
            x = newPos.x + p.x
            y = newPos.y + p.y
            if x < 0 or x > 9 or y > 20 or self.board[y][x] != 0:
                return False
        return True

    def checkX(self, dx):
        newPos = Point(self.pos.x + dx, self.pos.y)
        return newPos if self.checkPos(newPos, self.rotation) else self.pos

    def checkRot(self, dr):
        newRot = (self.rotation + dr) % 4
        return newRot if self.checkPos(self.pos, newRot) else self.rotation

    def drawPiece(self, color):
        self.playArea.attrset(curses.color_pair(color))
        for p in self.piece[self.rotation]:
            if p.y + self.pos.y > 0:
                self.playArea.addstr(p.y + self.pos.y, (p.x + self.pos.x)*2 + 1 , "  ")

    def loop(self):

        # Draw the piece
        self.drawPiece(2)

        self.playArea.refresh()

        # then erase for next frame
        self.drawPiece(1)

        ch = self.stdscr.getch()
        if ch == ord('q') or ch == ord('Q'): return False
        elif ch == curses.KEY_RIGHT: self.pos = self.checkX(1)
        elif ch == curses.KEY_LEFT: self.pos = self.checkX(-1)
        elif ch == curses.KEY_UP: self.rotation = self.checkRot(1)
        elif ch == curses.KEY_DOWN: self.pos = Point(self.pos.x, self.pos.y + 1)

        now = time.time()
        self.acc += now - self.then
        while self.acc > 1:
            self.pos = Point(self.pos.x, self.pos.y + 1)
            self.acc -= 1
        self.then = now
        return True

    def run(self, stdscr):

        self.stdscr = stdscr

        if curses.has_colors():
            bg = curses.COLOR_BLACK
            curses.init_pair(1, curses.COLOR_BLUE, bg)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_CYAN)

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

        self.piece = pieces['I']
        self.rotation = 0
        self.pos = Point(5,0)
        self.then = time.time()
        self.acc = 0.0
        while self.loop():
            pass

t = Tetris()
curses.wrapper(t.run)