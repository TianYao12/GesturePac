import cv2
import mediapipe as mp
import math

head_x, head_y = 0, 0
tail_x, tail_y = 0, 0

webcam = cv2.VideoCapture(1)
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
          elif (dx > 0 and dy < 0 and abs(dy) > abs(dx)) or (dx < 0 and dy < 0 and abs(dy) > abs(dx)):
            cv2.putText(image, 'up', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
          elif (dx > 0 and dy > 0 and abs(dy) <= abs(dx)) or (dx > 0 and dy < 0 and abs(dy) <= abs(dx)):
            cv2.putText(image, 'left', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
          elif (dx < 0 and dy > 0 and abs(dy) <= abs(dx)) or (dx < 0 and dy < 0 and abs(dy) <= abs(dx)):
            cv2.putText(image, 'right', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
    

        cv2.line(image, (head_x, head_y), (tail_x, tail_y), (0, 255, 0), 5)

        
  
  cv2.imshow("Gesture", image)

  key = cv2.waitKey(10)

  if key == 27:
    break

webcam.release()
cv2.destroyAllWindows()
