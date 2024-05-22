
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
            [Point(0,-2), Point(0, -1), Point(0,0), Point(0, 1)],
        ],
        'J' : [
            [Point(-1,0), Point(0,0), Point(1,0), Point(1, 1)],
            [Point(0,-1), Point(0,0), Point(0,1), Point(-1, 1)],
            [Point(1,0), Point(0,0), Point(-1,0), Point(-1, -1)],
            [Point(0,1), Point(0,0), Point(0,-1), Point(1, -1)],
        ],
        'L' : [
            [Point(-1,1), Point(-1,0), Point(0,0), Point(1, 0)],
            [Point(-1,-1), Point(0,-1), Point(0,0), Point(0, 1)],
            [Point(-1,0), Point(0,0), Point(1,0), Point(1, -1)],
            [Point(0,-1), Point(0,0), Point(0,1), Point(1, 1)]
        ],
        'T' : [
            [Point(-1,0), Point(0,0), Point(1,0), Point(0, 1)],
            [Point(-1,0), Point(0,0), Point(0,1), Point(0, -1)],
            [Point(-1,0), Point(0,0), Point(1,0), Point(0, -1)],
            [Point(0,-1), Point(0,0), Point(0,1), Point(1, 0)]
        ],
        'S' : [
            [Point(-1,1), Point(0,0), Point(0,1), Point(1, 0)],
            [Point(0,-1), Point(0,0), Point(1,0), Point(1, 1)],
            [Point(-1,1), Point(0,0), Point(0,1), Point(1, 0)],
            [Point(0,-1), Point(0,0), Point(1,0), Point(1, 1)]
        ],
        'Z' : [
            [Point(-1,0), Point(0,0), Point(0,1), Point(1, 1)],
            [Point(0,1), Point(0,0), Point(1,0), Point(1, -1)],
            [Point(-1,0), Point(0,0), Point(0,1), Point(1, 1)],
            [Point(0,1), Point(0,0), Point(1,0), Point(1, -1)],
        ],
        'O' : [
            [Point(-1,0), Point(0,0), Point(-1,1), Point(0, 1)],
            [Point(-1,0), Point(0,0), Point(-1,1), Point(0, 1)],
            [Point(-1,0), Point(0,0), Point(-1,1), Point(0, 1)],
            [Point(-1,0), Point(0,0), Point(-1,1), Point(0, 1)],
        ]

    }

colors = {
    'I' : 1,
    'J' : 2,
    'L' : 3,
    'T' : 4,
    'S' : 5,
    'Z' : 6,
    'O' : 7
}

scores = [40, 100, 300, 400]

class Tetris:
    def __init__(self):
        self.board = [[0 for x in range(10)] for y in range(20)]
        self.piece = None
        self.level = 1

    def checkPos(self, newPos, newRot):
        for p in pieces[self.piece][newRot]:
            x = newPos.x + p.x
            y = newPos.y + p.y
            if x < 0 or x > 9 or y > 19 or self.board[y][x] != 0:
                if y >= 0:
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

    def updateScore(self, lines):
        if lines == 0:
            return
        self.lines += lines
        self.level = min(((lines // 5) + 1), 12)
        self.score += scores[lines-1] * self.level
        self.drawScore()

    def lockPiece(self):
        for p in pieces[self.piece][self.rotation]:
            x = self.pos.x + p.x
            y = self.pos.y + p.y
            self.board[y][x] = colors[self.piece]
        fullCount = 0
        for y in range(20):
            full = True
            for x in range(10):
                if self.board[y][x] == 0:
                    full = False
                    break
            if full:
                fullCount += 1
                for y2 in reversed(range(0, y)):
                    self.board[y2+1] = self.board[y2]
                self.board[0] = [0 for x in range(10)]

        self.updateScore(fullCount)

        self.redrawBoard()
        self.choosePiece()

    def redrawBoard(self):
        self.playArea.attrset(curses.color_pair(0))
        self.playArea.border()
        for y in range(20):
            for x in range(10):
                self.playArea.attrset(curses.color_pair(self.board[y][x]))
                self.playArea.addstr(y + 1, (x*2) + 1 , "  ")
        self.playArea.refresh()

    def redrawPreview(self):
        self.previewArea.erase()
        self.previewArea.attrset(curses.color_pair(0))
        self.previewArea.border()
        self.previewArea.attrset(curses.color_pair(colors[self.nextpiece]))
        for p in pieces[self.nextpiece][0]:
            self.previewArea.addstr(p.y + 3, (p.x)*2 + 6 , "  ")
        self.previewArea.refresh()

    def drawScore(self):
        self.scoreArea.erase()
        self.scoreArea.border()
        self.scoreArea.addstr(1, 3, "Score")
        self.scoreArea.addstr(2, 3, str(self.score))
        self.scoreArea.addstr(4, 3, "Lines")
        self.scoreArea.addstr(5, 3, str(self.lines))
        self.scoreArea.addstr(7, 3, "level")
        self.scoreArea.addstr(8, 5, str(self.level))
        self.scoreArea.refresh()

    def drawPiece(self, color):
        self.playArea.attrset(curses.color_pair(color))
        for p in pieces[self.piece][self.rotation]:
            if p.y + self.pos.y >= 0:
                self.playArea.addstr(p.y + self.pos.y + 1, (p.x + self.pos.x)*2 + 1 , "  ")

    def choosePiece(self):
        if self.piece == None:
            self.piece = random.choice(['I', 'J', 'L', 'T', 'S', 'Z', 'O'])
        else:
            self.piece = self.nextpiece
        self.nextpiece = random.choice(['I', 'J', 'L', 'T', 'S', 'Z', 'O'])
        self.redrawPreview()
        self.rotation = 0
        self.pos = Point(5,0)
        if self.checkPos(self.pos, self.rotation) == False:
            self.done = True

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
        self.rate = pow(0.80, self.level)
        if self.acc > self.rate:
            self.acc = 0
            if self.checkDown():
                self.pos = Point(self.pos.x, self.pos.y + 1)
            else:
                self.lockPiece()
        self.then = now
        return not self.done

    def run(self, stdscr):

        self.stdscr = stdscr

        if curses.has_colors():
            fg = curses.COLOR_WHITE
            curses.init_pair(1, fg, 1)
            curses.init_pair(2, fg, 2)
            curses.init_pair(3, fg, 3)
            curses.init_pair(4, fg, 4)
            curses.init_pair(5, fg, 5)
            curses.init_pair(6, fg, 6)
            curses.init_pair(7, fg, 7)

        curses.nl()
        curses.noecho()
        curses.curs_set(0)

        stdscr.timeout(0)

        if curses.COLS < 40 or curses.LINES < 20:
            raise Exception("Need a bigger console")

        stdscr.refresh()
        self.playArea = curses.newwin(22, 22, (curses.LINES - 22) // 2, 1)
        self.previewArea = curses.newwin(7, 14, (curses.LINES - 22) // 2, 25)
        self.scoreArea = curses.newwin(10, 14, (curses.LINES - 22) // 2 + 10, 25)
        self.redrawBoard()

        self.choosePiece()
        self.then = time.time()
        self.acc = 0.0
        self.done = False
        self.lines = 0
        self.score = 0
        self.drawScore()
        while self.loop():
            pass

t = Tetris()
curses.wrapper(t.run)