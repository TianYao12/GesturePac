import pygame as py
import math
from board import boards as boardMap

py.init()

CELLSIZE = 20
CELLX = 30
CELLY = 33
WIDTH = CELLSIZE * CELLX
HEIGHT = CELLSIZE * CELLY
FPS = 60
COLOURTHEME = 'blue'

screen = py.display.set_mode([WIDTH, HEIGHT])
timer = py.time.Clock()
player_images = []
for i in range(1, 5):
    player_images.append(py.transform.scale(py.image.load(f'assets/player_images/{i}.png'), (CELLSIZE, CELLSIZE)))

board_images = []
for i in range(1, 10):
    board_images.append(py.transform.scale(py.image.load(f'assets/board_images/{i}.png').convert_alpha(), (CELLSIZE, CELLSIZE)))

flicker = True

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.dir = 0
    def update(self):
        self.x += math.cos(math.radians(self.dir))
        self.y -= math.sin(math.radians(self.dir))
    def display(self):
            # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        screen.blit(py.transform.rotate(player_images[0], self.dir), (self.x, self.y))

player = Player()

class Tile:
    def __init__(self, type):
        self.type = type

    def display(self, x, y):
        if self.type >= 1:
            screen.blit(board_images[self.type-1], (x,y))




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
                player.dir = 0
            if e.key == py.K_UP:
                player.dir = 90
            if e.key == py.K_LEFT:
                player.dir = 180
            if e.key == py.K_DOWN:
                player.dir = 270
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
