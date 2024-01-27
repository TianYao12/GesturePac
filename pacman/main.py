import numpy as np  
import cv2
import pygame as py
import math
from board import boards as boardMap
import threading
import queue
import os
import mediapipe as mp

os.chdir("./pacman/")

signIndex = 0

def run_model(q):
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0

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
                        
                    dx = head_x - tail_x
                    dy = head_y - tail_y
                    dist = (dx**2 + dy**2)**(0.5)

                    if dist > 110:      #threshold for pointing detection
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
        def __init__(self, x=15, y=24):
            self.x = x
            self.y = y
            self.dir = 0
            self.queuedDir = None
        def update(self):

            if not(self.x % 1 == 0 and self.y % 1 == 0) or board[int(self.y - sin(self.dir))][int(self.x + cos(self.dir))].type < 3:
                self.x = round(self.x + 0.05 * cos(self.dir), 2)
                self.y = round(self.y - 0.05 * sin(self.dir), 2)
            if self.x % 1 == 0 and self.y % 1 == 0:
                self.checkTurns()
                if board[int(self.y)][int(self.x)].type < 3:
                    board[int(self.y)][int(self.x)].type = 0


            # print(self.x, self.y)
        def display(self):
            screen.blit(py.transform.rotate(player_images[0], self.dir), (self.x * CELLSIZE, self.y * CELLSIZE))
            py.draw.circle(screen, 'white', (self.x * CELLSIZE, self.y * CELLSIZE), 3)
        def checkTurns(self):
            if self.queuedDir == None:
                pass
            
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
        def __init__(self, name='a', x=18, y=24):
            self.name = name
            self.x = x
            self.y = y
            self.dir = 0
        def update(self):
            

            if self.x % 1 == 0 and self.y % 1 == 0:
                self.checkTurns()
            self.x = round(self.x + 0.04 * cos(self.dir), 2)
            self.y = round(self.y + 0.04 * sin(self.dir), 2)


        def display(self):
            py.draw.circle(screen, 'white', (self.x * CELLSIZE + CELLSIZE/2, self.y * CELLSIZE + CELLSIZE/2), 10)
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

            end_node = Node(None, (int(player.x), int(player.y)))
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
                        py.draw.circle(screen, 'white', (current_node.position[0] * CELLSIZE + CELLSIZE/2, current_node.position[1] * CELLSIZE + CELLSIZE/2), 7)
                        current_node = current_node.parent
                    return path[::-1]
                
                children = []
                for relative_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_position = (current_node.position[0] + relative_position[0], current_node.position[1] + relative_position[1])
                    if board[new_position[1]][new_position[0]].type >= 3 or new_position[0] < 0 or new_position[0] > CELLX:
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

    # I don't think this works
    # class QGhost:
    #     def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1, x=18, y=24):
    #         self.x = x
    #         self.y = y
    #         self.q_table = defaultdict(lambda: np.zeros(4))
    #         self.learning_rate = learning_rate
    #         self.discount_factor = discount_factor
    #         self.exploration_rate = exploration_rate

    #     def update(self):
    #         self.checkTurns()
    #         if self.x % 1 == 0 and self.y % 1 == 0:
    #             self.checkTurns()
    #         self.x = round(self.x + 0.05 * cos(self.dir), 2)
    #         self.y = round(self.y + 0.05 * sin(self.dir), 2)

    #     def display(self):
    #         py.draw.circle(screen, 'white', (self.x * CELLSIZE + CELLSIZE/2, self.y * CELLSIZE + CELLSIZE/2), 10)

    #     def checkTurns(self):
    #         state = self.get_state()
    #         action = self.get_action(state)
    #         reward = self.get_reward()

    #         next_state = self.get_state()
    #         next_action = self.get_action(next_state)

    #         q_value = self.q_table[state][action]
    #         next_q_value = self.q_table[next_state][next_action]
    #         td_error = reward + self.discount_factor * next_q_value - q_value
    #         self.q_table[state][action] += self.learning_rate * td_error
    #         print(self.q_table[state][action])
    #         self.dir = 90 * action

    #     def get_state(self):
            
    #         dx = round(30*(player.x - self.x))
    #         dy = round(30*(player.y - self.y))
    #         state = dx, dy
    #         return state
    #     def get_action(self,state):
    #         if np.random.rand() < self.exploration_rate:
    #             action = np.random.randint(0,4)
    #         else:
    #             action = np.argmax(self.q_table[state])
    #         return action
        
    #     def get_reward(self):
    #         dx = player.x - self.x
    #         dy = player.x - self.y
    #         dist = math.hypot(3*dx, 3*dy)
    #         return -dist
        

    #     def get_direction(self, action):
    #         if action == 0:
    #             return 1, 0
    #         elif action == 1:
    #             return -1, 0
    #         elif action == 2:
    #             return 0, 1
    #         else:
    #             return 0, -1



        
                

    class Tile:
        def __init__(self, type):
            self.type = type

        def display(self, x, y):
            if self.type >= 1:
                screen.blit(board_images[self.type-1], (x ,y - 0 * CELLSIZE))


    board = []
    player = Player()
    g1 = astarGhost()
    def init():
        for i in range(0, CELLY):
            board.append([])
            for j in range(0, CELLX):
                board[i].append(Tile(boardMap[i][j]))

    def update():
        for e in py.event.get():
            if e.type == py.QUIT:
                #running
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
            print(vall)
            player.queuedDir = vall * 90
        player.update()
        g1.update()

    def display():
        player.display()
        g1.display()

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


q = queue.Queue()


pygame_thread = threading.Thread(target=run_game, args=(q,))
opencv_thread = threading.Thread(target=run_model, args=(q,))

# Start the threads
pygame_thread.start()
opencv_thread.start()

# Wait for both threads to complete
pygame_thread.join()
opencv_thread.join()

