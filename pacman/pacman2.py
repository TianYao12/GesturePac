import pygame as py
import math
from board import boards as boardMap

py.init()

CELLSIZE = 22
CELLX = 30
CELLY = 33
WIDTH = CELLSIZE * CELLX
HEIGHT = CELLSIZE * CELLY
FPS = 60
COLOURTHEME = 'blue'
def cos(n): return round(math.cos(math.radians(n)))
def sin(n): return round(math.sin(math.radians(n)))


screen = py.display.set_mode([WIDTH, HEIGHT])
timer = py.time.Clock()
player_images = []
for i in range(1, 5):
    player_images.append(py.transform.scale(py.image.load(f'assets/player_images/{i}.png'), (CELLSIZE, CELLSIZE)))

board_images = []
for i in range(1, 10):
    board_images.append(py.transform.scale(py.image.load(f'assets/board_images/{i}.png').convert_alpha(), (CELLSIZE, CELLSIZE)))


score = 0
flicker = True

class Player:
    def __init__(self):
        self.x = 15
        self.y = 24
        self.dir = 0
        self.queuedDir = None
    def update(self):

        

        if self.x % 1 == 0 and self.y % 1 == 0:
            self.checkTurns()
            if board[int(self.y - sin(self.dir))][int(self.x + cos(self.dir))].type < 3:
                self.x = round(self.x + 0.05 * cos(self.dir), 2)
                self.y = round(self.y - 0.05 * sin(self.dir), 2)
            if board[int(self.y)][int(self.x)].type < 3:
                board[int(self.y)][int(self.x)].type = 0

        else:
            self.x = round(self.x + 0.05 * cos(self.dir), 2)
            self.y = round(self.y - 0.05 * sin(self.dir), 2)

        print(self.x, self.y)
    def display(self):
        screen.blit(py.transform.rotate(player_images[0], self.dir), (self.x * CELLSIZE- 2*CELLSIZE, self.y * CELLSIZE - 2* CELLSIZE))
        py.draw.circle(screen, 'white', (self.x * CELLSIZE - 1.5*CELLSIZE, self.y * CELLSIZE- 1.5*CELLSIZE), 3)
    def checkTurns(self):
        if self.queuedDir == None:
            pass
        
        elif board[int(self.y - sin(self.queuedDir))][int(self.x + cos(self.queuedDir))].type < 3:
            self.dir = self.queuedDir
            self.queuedDir = None

        
        

player = Player()

class Tile:
    def __init__(self, type):
        self.type = type

    def display(self, x, y):
        if self.type >= 1:
            screen.blit(board_images[self.type-1], (x- 1.5*CELLSIZE,y- 1.5*CELLSIZE))


board = []


def init():
    for i in range(0, CELLY):
        board.append([])
        for j in range(0, CELLX):
            board[i].append(Tile(boardMap[i][j]))

def update():
    for e in py.event.get():
        if e.type == py.QUIT:
            running
            running = False
        if e.type == py.KEYDOWN:
            if e.key == py.K_RIGHT:
                player.queuedDir = 0
            if e.key == py.K_UP:
                player.queuedDir = 90
            if e.key == py.K_LEFT:
                player.queuedDir = 180
            if e.key == py.K_DOWN:
                player.queuedDir = 270
    player.update()

def display():
    player.display()

    for i in range(0, CELLY):
        for j in range(0, CELLX):
            board[i][j].display(j * CELLSIZE, i*CELLSIZE)


    # print("FPS:", int(timer.get_fps()))
    
    
running = True
if __name__ == "__main__":
    init()
    while running:
        timer.tick(FPS)
        screen.fill('black')
        update()
        display()
        py.display.flip()
    py.quit()
