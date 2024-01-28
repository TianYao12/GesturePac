import cv2 
import numpy as np
import tensorflow
import time
import random
import pygame
import pygame_textinput as pyti
import math
import threading
import queue
import os
import mediapipe as mp
os.chdir('./nostalgia/flappy')


def run_model(q):
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0


    webcam = cv2.VideoCapture(0)
    my_hands = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    counter = 0
    prev = 4
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

                # Shoelace theorem to find area in proportion with spread

                mean_x, mean_y = 0, 0
                cnt = 0

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    mean_x += x
                    mean_y += y
                    cnt += 1

                    if id == 0:
                        cv2.circle(img = image, center = (x, y), radius = 8, color = (0, 255, 255), thickness = 3)
                        head_x, head_y = x, y

                    if id == 12:
                        cv2.circle(img = image, center = (x, y), radius = 8, color = (0, 255, 255), thickness = 3)
                        tail_x, tail_y = x, y

                long_dist = (((head_x - tail_x)) ** 2 + (head_y - tail_y) ** 2) ** (0.5)
                mean_x, mean_y = int(mean_x / cnt), int(mean_y / cnt)

                spread_distance = 0
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    spread_distance += (((mean_x - x) ** 2) + ((mean_y - y)**2)) ** 0.5

                spread_distance /= 21     # dividing by number of landmarks in mediapipe
                    
                print(spread_distance / long_dist)      # note the multiplication bc spread and long dist both increase
                if spread_distance / long_dist < 0.4:
                    cv2.putText(image, 'open', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                    if (prev!=1):
                        q.put(1)
                        prev=1
                    # open
                else:
                    cv2.putText(image, 'close', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
                    if (prev!=0):
                        q.put(0)
                        prev=0
                    #close
                    
        
        cv2.imshow("Gesture", image)

        key = cv2.waitKey(10)

        if key == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


def run_game(q):
  time.sleep(9)
  pygame.init()

  SCREEN = pygame.display.set_mode((500, 750))

  BACKGROUND_IMAGE = pygame.image.load('assets/background.jpg')

  BIRD_IMAGE = pygame.image.load('assets/bird1.png')
  bird_x = 50
  bird_y = 300
  bird_dy = 0

  def display_bird(x,y):
    SCREEN.blit(BIRD_IMAGE, (x, y))


  OBSTACLE_WIDTH = 50
  OBSTACLE_HEIGHT = random.randint(50, 250)
  OBSTACLE_COLOR = (211, 253, 117)
  OBSTACLE_DX = -0.3
  obstacle_x = 500

  def display_obstacle(height):
      pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, height))
      bottom_obstacle_height = 635 - (height + 350)
      pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, height + 350, OBSTACLE_WIDTH, bottom_obstacle_height))


  def collision_detection (obstacle_x, obstacle_height, bird_y, bottom_obstacle_height):
    if obstacle_x >= 50 and obstacle_x <= (50 + 64):
      if bird_y <= obstacle_height or bird_y >= (bottom_obstacle_height - 64):
        return True
    return False

  score = 0

  SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)

  def score_display(score):
    display = SCORE_FONT.render(f"score: {score}", True, (255, 255, 255))
    SCREEN.blit(display, (10, 10))


  running = True
  while running:
    SCREEN.fill((0,0,0))

    # display the background image
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not collision:
               bird_dy = -1.2

    if  not(q.empty()):
            vall = q.get()
            if vall == 0:
               bird_dy = -1.2



    bird_y += bird_dy
    bird_dy += 0.005

    if bird_y <= 0:
      bird_y = 0
    if bird_y >= 571:
      bird_y = 571

    # Moving the obstacle
    obstacle_x += OBSTACLE_DX

      # COLLISION
      
      # generating new obstacles
    if obstacle_x <= -10:
        obstacle_x = 500
        OBSTACLE_HEIGHT = random.randint(50, 250)
        score += 1
    # displaying the obstacle
    display_obstacle(OBSTACLE_HEIGHT)

    collision = collision_detection(obstacle_x, OBSTACLE_HEIGHT, bird_y, OBSTACLE_HEIGHT + 350)

    if collision:
      bird_dy = 0
      OBSTACLE_DX = 0
      running = False

    display_bird(bird_x, bird_y)

    score_display(score)
    
    pygame.display.update()

  
  textinput = pyti.TextInputVisualizer(font_color='white', cursor_color='white')
  font = pygame.font.Font('freesansbold.ttf', 24)
  waiting = True
  while waiting:
    SCREEN.fill('black')

    events = pygame.event.get()

    textinput.update(events)
    tirect = textinput.surface.get_rect(center=(500/2, 750/2))
    SCREEN.blit(textinput.surface, tirect)

    name = textinput.value


    t1 = font.render(f"CONGRATS! YOUR FINAL SCORE IS {score}", True, 'white')
    t1rect = t1.get_rect(center=(500/2, 750/2 + 200))
    SCREEN.blit(t1, t1rect)

    t2 = font.render("ENTER YOUR NAME", True, 'white')
    t2rect = t2.get_rect(center=(500/2, 750/2 + 100))
    SCREEN.blit(t2, t2rect)
            
    pygame.display.flip()
    for e in events:
      if e.type == pygame.QUIT:
        exit()
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_RETURN:
          waiting = False
            
  print(name) # NAME INPUT VARIABLE

  pygame.quit()
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