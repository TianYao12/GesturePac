import numpy as np  
import time
import pygame as py
import pygame_textinput as pyti
import math
from board import boards as boardMap
import threading
import queue
import os
import mediapipe as mp
import cv2

os.chdir("./nostalgia/pacman/") # THIS IS FOR TESTING PURPOSES ONLY


signIndex = 0



def run_model(q):
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0
    wrist_x, wrist_y = 0, 0

    webcam = cv2.VideoCapture(0)
    my_hands = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    counter = 0
    while True:
        success, image = webcam.read()
        frame_height, frame_width, channels = image.shape
        rgb_image =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_image)

        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(image, hand)
                landmarks = hand.landmark
                prev = 4
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:                               # top of index finger
                        cv2.circle(img = image, center = (x, y), radius = 8, color = (0, 255, 255), thickness = 3)
                        head_x = x
                        head_y = y
                    if id == 5:
                        cv2.circle(img = image, center = (x, y), radius = 8, color = (0, 255, 255), thickness = 3)
                        tail_x = x
                        tail_y = y
                    if id == 0:
                        wrist_x = x
                        wrist_y = y
                        
                    dx = head_x - tail_x
                    dy = head_y - tail_y
                    wrist_dist = (((head_x - wrist_x) ** 2) + (head_y - wrist_y) ** 2) ** (0.5)
                    dist = (dx**2 + dy**2)**(0.5)

                    if dist / wrist_dist > 0.25:      #threshold for pointing detection
                        # print(counter)      45 degrees is the threshold for changing direction
                        if (dx > 0 and dy > 0 and abs(dy) > abs(dx)) or (dx < 0 and dy > 0 and abs(dy) > abs(dx)): 
                            cv2.putText(image, 'down', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                            if (prev!=3):
                                q.put(3)
                                prev=3
                            #3
                        elif (dx > 0 and dy < 0 and abs(dy) > abs(dx)) or (dx < 0 and dy < 0 and abs(dy) > abs(dx)):
                            cv2.putText(image, 'up', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                            if (prev!=1):
                                q.put(1)
                                prev=1
                            #1
                        elif (dx > 0 and dy > 0 and abs(dy) <= abs(dx)) or (dx > 0 and dy < 0 and abs(dy) <= abs(dx)):
                            cv2.putText(image, 'left', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                            if (prev!=2):
                                q.put(2)
                                prev=2
                            #2
                        elif (dx < 0 and dy > 0 and abs(dy) <= abs(dx)) or (dx < 0 and dy < 0 and abs(dy) <= abs(dx)):
                            cv2.putText(image, 'right', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                            if (prev!=0):
                                q.put(0)
                                prev=0
                            #0
                    

                    cv2.line(image, (head_x, head_y), (tail_x, tail_y), (0, 255, 0), 5)

                    
            
        cv2.imshow("Gesture", image)

        key = cv2.waitKey(10)

        if key == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


def run_game(q):
    py.init()

    py.mixer.init()
    py.mixer.music.load('assets/bg.mp3')
    py.mixer.music.set_volume(0.3)
    py.mixer.music.play()

    CELLSIZE = 22
    CELLX = 30
    CELLY = 33
    WIDTH = CELLSIZE * CELLX
    HEIGHT = CELLSIZE * CELLY
    FPS = 60
    COLOURTHEME = 'blue'
    def cos(n): return round(math.cos(math.radians(n)))
    def sin(n): return round(math.sin(math.radians(n)))

    screen = py.display.set_mode([WIDTH + 200, HEIGHT])
    timer = py.time.Clock()
    font = py.font.Font('freesansbold.ttf', 24)

    player_images = []
    for i in range(1, 5):
        player_images.append(py.transform.scale(py.image.load(f'assets/player_images/{i}.png'), (CELLSIZE, CELLSIZE)))

    board_images = []
    for i in range(1, 10):
        board_images.append(py.transform.scale(py.image.load(f'assets/board_images/{i}.png').convert_alpha(), (CELLSIZE, CELLSIZE)))

    def outofx(x):
        return x < 0 or x >= CELLX
    def outofy(y):
        return y < 0 or y >= CELLY


    class Player:
        def __init__(self):
            self.homex = 15
            self.homey = 24
            self.x = self.homex
            self.y = self.homey
            self.dir = 0
            self.queuedDir = None
            self.score = 0
            self.flicker = 0
            self.lives = 3
        def update(self):
            
            if self.flicker > 0:
                self.flicker -= 1
            
            if outofy(int(self.y - sin(self.dir))) or outofx(int(self.x + cos(self.dir))) :
                self.x = round(self.x + 0.05 * cos(self.dir), 2) % (CELLX-0.05)
                self.y = round(self.y - 0.05 * sin(self.dir), 2) % CELLY
            elif not(self.x % 1 == 0 and self.y % 1 == 0) or board[int(self.y - sin(self.dir))][int(self.x + cos(self.dir))].type < 3:
                self.x = round(self.x + 0.05 * cos(self.dir), 2) % (CELLX-0.05)
                self.y = round(self.y - 0.05 * sin(self.dir), 2) % CELLY

            if self.x % 1 == 0 and self.y % 1 == 0:
                self.checkTurns()
                if board[int(self.y)][int(self.x)].type < 3:
                    if board[int(self.y)][int(self.x)].type == 1:
                        self.score += 10
                    elif board[int(self.y)][int(self.x)].type == 2:
                        self.score += 50
                        self.flicker = 360
                    board[int(self.y)][int(self.x)].type = 0
                    


            # print(self.x, self.y)
        def display(self):
            screen.blit(py.transform.rotate(player_images[0], self.dir), (self.x * CELLSIZE, self.y * CELLSIZE))
        def checkTurns(self):
            if self.queuedDir == None:
                pass
            elif outofy(int(self.y - sin(self.dir))) or outofx(int(self.x + cos(self.dir))):
                self.dir = self.queuedDir
                self.queuedDir = None
            elif board[int(self.y - sin(self.queuedDir))][int(self.x + cos(self.queuedDir))].type < 3:
                self.dir = self.queuedDir
                self.queuedDir = None

    class Node():
        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position
            
            self.a = 0
            self.b = 0
            self.c = 0
        def __eq__(self,other):
            return self.position == other.position

    class astarGhost:
        def __init__(self, name='blinky'):
            self.name = name
            self.dir = 0
            self.alive = True
            self.weakImage = py.transform.scale(py.image.load('assets/ghost_images/powerup.png'), (CELLSIZE, CELLSIZE))
            self.deadImage = py.transform.scale(py.image.load('assets/ghost_images/dead.png'), (CELLSIZE, CELLSIZE))
            if name == 'blinky':
                self.color = "red"
                self.speed = 0.025
                self.homex = 14
                self.homey = 13
                self.image = py.transform.scale(py.image.load('assets/ghost_images/red.png'), (CELLSIZE, CELLSIZE))
            elif name == 'pinky':
                self.color = "pink"
                self.speed = 0.03125
                self.homex = 12
                self.homey = 16
                self.image = py.transform.scale(py.image.load('assets/ghost_images/pink.png'), (CELLSIZE, CELLSIZE))
            elif name == 'inky':
                self.color = "cyan"
                self.speed = 0.03125
                self.homex = 14
                self.homey = 16
                self.image = py.transform.scale(py.image.load('assets/ghost_images/blue.png'), (CELLSIZE, CELLSIZE))
            elif name == 'clyde':
                self.color = "orange"
                self.speed = 0.04
                self.homex = 14
                self.homey = 16
                self.image = py.transform.scale(py.image.load('assets/ghost_images/orange.png'), (CELLSIZE, CELLSIZE))

            self.x = self.homex
            self.y = self.homey
        def update(self):
            
            if self.alive:
                if self.x % 1 == 0 and self.y % 1 == 0:
                    self.checkTurns()
                self.x = round(self.x + self.speed * cos(self.dir), 5)
                self.y = round(self.y + self.speed * sin(self.dir), 5)
            else:
                path = self.astar()
                if len(path) <= 1:
                    self.alive = True
                else:
                    self.x = path[1][0]
                    self.y = path[1][1]




        def display(self):
            if not(self.alive):
                screen.blit(self.deadImage,(self.x * CELLSIZE , self.y * CELLSIZE ))
            elif player.flicker == 0:
                # py.draw.circle(screen, self.color, (self.x * CELLSIZE + CELLSIZE/2, self.y * CELLSIZE + CELLSIZE/2), 10)
                screen.blit(self.image, (self.x * CELLSIZE , self.y * CELLSIZE ))
            else:
                # py.draw.circle(screen, 'white', (self.x * CELLSIZE + CELLSIZE/2, self.y * CELLSIZE + CELLSIZE/2), 10)
                screen.blit(self.weakImage, (self.x * CELLSIZE , self.y * CELLSIZE ))
        def checkTurns(self):

            path = self.astar()
            if len(path) <= 1:
                return
            self.dir = math.degrees(math.atan2(( path[1][1] - int(self.y)), (path[1][0] - int(self.x))))
            

        def astar(self):
            visited = []
            neighboring = []
            start_node = Node(None, (int(self.x), int(self.y)))
            start_node.c = start_node.b = start_node.a = 0
            if not(self.alive):
                end_node = Node(None, (int(self.homex), self.homey))
            elif self.name == 'blinky':
                end_node = Node(None, (int(player.x), int(player.y)))
            elif self.name == 'pinky':
                if math.hypot(self.x - player.x, self.y - player.y) < 6:
                    end_node = Node(None, (int(player.x), int(player.y)))
                else:
                    for i in range(19):
                        x,y = int(player.x + i*cos(player.dir)), int(player.y - i*sin(player.dir))
                        if outofy(y) or outofx(x):
                            break
                        if board[y][x].type >= 3:
                            break
                        end_node = Node(None, (x, y))
            elif self.name == 'inky':
                if math.hypot(self.x - player.x, self.y - player.y) < 8:
                    end_node = Node(None, (int(player.x), int(player.y)))
                else:
                    for i in range(19):
                        x,y = int(player.x - i*cos(player.dir)), int(player.y + i*sin(player.dir))
                        if outofy(y) or outofx(x):
                            break
                        if board[y][x].type >= 3:
                            break
                        end_node = Node(None, (x, y))
            elif self.name == 'clyde':
                if math.hypot(self.x - player.x, self.y - player.y) < 7:
                    end_node = Node(None, (int(player.x), int(player.y)))
                else:
                    end_node = Node(None, (int(CELLX - player.x - 1), int(player.y)))

            end_node.c = end_node.b = end_node.a = 0
            
            neighboring.append(start_node)
            
            while len(neighboring) > 0:
                current_node = neighboring[0]
                current_index = 0
                for i, v in enumerate(neighboring):
                    if v.c < current_node.c:
                        current_node = v
                        current_index = i
                neighboring.pop(current_index)
                visited.append(current_node)

                if current_node == end_node:
                    path = []
                    while current_node is not None:
                        path.append(current_node.position)
                        # py.draw.circle(screen, 'white', (current_node.position[0] * CELLSIZE + CELLSIZE/2, current_node.position[1] * CELLSIZE + CELLSIZE/2), 7)
                        current_node = current_node.parent
                    return path[::-1]
                
                children = []
                for relative_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_position = (current_node.position[0] + relative_position[0], current_node.position[1] + relative_position[1])
                    if board[new_position[1]][new_position[0]].type <= 8 and board[new_position[1]][new_position[0]].type >= 3 or new_position[0] < 0 or new_position[0] > CELLX:
                        continue
                    new_node = Node(current_node, new_position)
                    children.append(new_node)


                for child in children:
                    skip = False
                    for visited_node in visited:
                        if child == visited_node:
                            skip = True

                    child.a = current_node.a + 1
                    child.b = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                    child.c = child.a + child.b

                    for neighbor in neighboring:
                        if child == neighbor and child.a > neighbor.a:
                            skip = True
                    if not(skip):
                        neighboring.append(child)


    class Tile:
        def __init__(self, type):
            self.type = type

        def display(self, x, y):
            if self.type >= 1:
                screen.blit(board_images[self.type-1], (x, y - 0 * CELLSIZE))


    board = []
    player = Player()
    blinky = astarGhost("blinky")
    pinky = astarGhost("pinky")
    inky = astarGhost("inky")
    clyde = astarGhost("clyde")
    ghosts = [blinky, pinky, inky, clyde]


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
        if not(q.empty()):
            vall = q.get()
            print(vall * 90)
            player.queuedDir = vall * 90
        player.update()
        for ghost in ghosts:
            ghost.update()
            if math.hypot(player.x - ghost.x, player.y - ghost.y) < 1:
                if player.flicker > 0:
                    if ghost.alive:
                        player.score += 100
                        ghost.alive = False
                else:
                    player.lives -= 1
                    player.x, player.y = player.homex, player.homey
                    blinky.x = blinky.homex
                    blinky.y = blinky.homey
                    pinky.x =  pinky.homex
                    pinky.y =  pinky.homey
                    inky.x =   inky.homex
                    inky.y =   inky.homey
                    clyde.x =  clyde.homex
                    clyde.y =  clyde.homey
            

    def display():
        player.display()
        for ghost in ghosts:
            ghost.display()

        for i in range(0, CELLY):
            for j in range(0, CELLX):
                board[i][j].display(j * CELLSIZE, i*CELLSIZE)


        screen.blit(font.render(f"Lives: {player.lives}",True, 'white'), (CELLX * CELLSIZE + 30, CELLY * CELLSIZE/2 - 60))
        screen.blit(font.render(f"Score: {player.score}",True, 'white'), (CELLX * CELLSIZE + 30, CELLY * CELLSIZE/2 - 10))
        
    running = True
    if __name__ == "__main__":
        name = "John Cena"
        init()
        while running:
            timer.tick(FPS)
            screen.fill('black')
            update()
            display()
            py.display.flip()
            if player.lives <= 0:
                running = False
        textinput = pyti.TextInputVisualizer(font_color='white', cursor_color='white')
        waiting = True
        while waiting:
            screen.fill('black')
            timer.tick(FPS)
            

            events = py.event.get()

            textinput.update(events)
            tirect = textinput.surface.get_rect(center=((WIDTH + 200)/2, HEIGHT/2))
            screen.blit(textinput.surface, tirect)

            name = textinput.value


            t1 = font.render(f"CONGRATS! YOUR FINAL SCORE IS {player.score}", True, 'white')
            t1rect = t1.get_rect(center=((WIDTH + 200)/2, HEIGHT/2 + 200))
            screen.blit(t1, t1rect)

            t2 = font.render("ENTER YOUR NAME", True, 'white')
            t2rect = t2.get_rect(center=((WIDTH + 200)/2, HEIGHT/2 + 100))
            screen.blit(t2, t2rect)
            
            py.display.flip()
            for e in events:
                if e.type == py.QUIT:
                    exit()
                if e.type == py.KEYDOWN:
                    if e.key == py.K_RETURN:
                        waiting = False
            
        print(name) # NAME INPUT VARIABLE

        py.quit()
        exit()


q = queue.Queue()


pygame_thread = threading.Thread(target=run_game, args=(q,))
opencv_thread = threading.Thread(target=run_model, args=(q,))

# Start the threads
pygame_thread.start()
opencv_thread.start()

# Wait for both threads to complete
pygame_thread.join()
opencv_thread.join()
