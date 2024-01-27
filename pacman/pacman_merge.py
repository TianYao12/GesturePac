from turtle import update
import pygame as py
import math
from board import boards as boardMap
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import tensorflow
import time
import threading


from multiprocessing import Process, Queue
from pacman.pacman2 import init

def hand_gesture_recognition(queue):
    cap = cv2.VideoCapture(1)

    detector = HandDetector(maxHands = 1)
    classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')

    # offset for the image crop
    offset = 30

    imgSize = 300

    folder = "Data/right"
    counter = 0

    labels = ['up', 'down', 'left', 'right']

    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            # get bounding box info
            x, y, w, h = hand['bbox']
            #print(x, y, w, h)
            # 1x255 gives white
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]
            imgCropShape = imgCrop.shape

            #TODO: handle case where hand is too big for screen

            aspectRatio = h/w
            if aspectRatio > 1:                 # in this case the height of image is larger than width
                k = imgSize / h                   # how much to shift width by
                wCal = int(k * w) + 1             # ceil
                
                imgResize = cv2.resize(imgCrop,(wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = int((300 - wCal) / 2) + 1
                try:
                    imgWhite[:, wGap: wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite)
                    print(prediction, index)
                except ValueError as e:
                    cv2.putText(img, 'move away from camera', (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0,255),1)
            
        else: # width of the image is larger than the height
            k = imgSize / w
            hCal = int(k * h) + 1

            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imResizeShape = imgResize.shape
            hGap = int((imgSize - hCal) / 2) + 1
            try:
                imgWhite[hGap:hGap + hCal, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite)
                print(prediction, index)
                queue.put(prediction)
            except ValueError as e:
                cv2.putText(img, 'move away from camera', (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0,255),1)

        cv2.putText(imgOutput, labels[index], (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

        cv2.imshow('Imagecrop', imgCrop)
        cv2.imshow('ImageWhite', imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)

    #TODO: try except for the hand being outside of the screen
        # Put the recognized gesture into the queue

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

player = Player() # Create an instance of the Player class

class Tile:
    def __init__(self, type):
        self.type = type

    def display(self, x, y):
        if self.type >= 1:
            screen.blit(board_images[self.type-1], (x- 1.5*CELLSIZE,y- 1.5*CELLSIZE))

board = []

def display():
    player.display()

    for i in range(0, CELLY):
        for j in range(0, CELLX):
            board[i][j].display(j * CELLSIZE, i*CELLSIZE)

def pacman_game(q, player):
    recognized_gesture = q.get() # gets first que prediction value from hand_gesture_recognition
    if recognized_gesture == 'up':
        player.queuedDir = 90
    elif recognized_gesture == 'down':
        player.queuedDir = 270
    elif recognized_gesture == 'left':
        player.queuedDir = 180
    elif recognized_gesture == 'right':
        player.queuedDir = 0


def main():
    q = Queue() # passes information between hand_gesture_recognition and pacman_game
    p = Process(target=hand_gesture_recognition, args=(q,)) # runs hand_gesture_recognition and passes q as param
    p.start()

    init()

    recognition_thread = threading.Thread(target=hand_gesture_recognition, args=(q,))
    recognition_thread.start()
    
    running = True
    while running:
        timer.tick(FPS)
        screen.fill('black')
        update()
        display()
        pacman_game(q, player)  # Incorporate the pacman_game logic here
        py.display.flip()

    p.terminate()  # Terminate the hand_gesture_recognition process when the game loop ends
    recognition_thread.join()  # Wait for the recognition_thread to finish
    py.quit()

if __name__ == "__main__":
    main()