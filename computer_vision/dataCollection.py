import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time



cap = cv2.VideoCapture(1)

detector = HandDetector(maxHands = 1)

# offset for the image crop
offset = 30

imgSize = 300

folder = "Data/right"
counter = 0

while True:
  success, img = cap.read()

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
      except ValueError as e:
        cv2.putText(img, 'move away from camera', (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0,255),1)
    
    else:
      k = imgSize / w
      hCal = int(k * h) + 1

      imgResize = cv2.resize(imgCrop, (imgSize, hCal))
      imResizeShape = imgResize.shape
      hGap = int((imgSize - hCal) / 2) + 1
      try:
        imgWhite[hGap:hGap + hCal, :] = imgResize
      except ValueError as e:
        cv2.putText(img, 'move away from camera', (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0,255),1)


    cv2.imshow('Imagecrop', imgCrop)
    cv2.imshow('ImageWhite', imgWhite)

  cv2.imshow("Image", img)
  key = cv2.waitKey(1)
  if key == ord("s"):
    counter += 1
    cv2.imwrite(f"{folder}/Image_{time.time()}.jpg", imgWhite)
    print(counter)

#TODO: try except for the hand being outside of the screen