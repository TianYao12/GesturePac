import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import tensorflow
import time
import requests


cap = cv2.VideoCapture(1)

detector = HandDetector(maxHands=1)
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
        # print(x, y, w, h)
        # 1x255 gives white
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]
        imgCropShape = imgCrop.shape

        # TODO: handle case where hand is too big for screen

        aspectRatio = h/w
        if aspectRatio > 1:                 # in this case the height of image is larger than width
            k = imgSize / h                   # how much to shift width by
            wCal = int(k * w) + 1             # ceil
            try:
              imgResize = cv2.resize(imgCrop, (wCal, imgSize))
              imgResizeShape = imgResize.shape
            except:
              continue

            wGap = int((300 - wCal) / 2) + 1
            try:
                imgWhite[:, wGap: wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite)
                # print(prediction, index)
                response = requests.post(
                    "http://127.0.0.1:8000/data/", json={"direction": labels[index]})
            except ValueError as e:
                cv2.putText(img, 'move away from camera', (20, 20),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

        else:  # width of the image is larger than the height
            k = imgSize / w
            hCal = int(k * h) + 1

            try:
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imResizeShape = imgResize.shape
            except:
                continue
            hGap = int((imgSize - hCal) / 2) + 1
            try:
                imgWhite[hGap:hGap + hCal, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite)
                #print(prediction, index)
                # with open('thumb_direction.txt', 'w') as file:
                #   file.write(str(labels[index]))
                response = requests.post(
                    "http://127.0.0.1:8000/data/", json={"direction": labels[index]})
                # print(f"response postsed:{response}")

            except ValueError as e:
                cv2.putText(img, 'move away from camera', (20, 20),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

        cv2.putText(imgOutput, labels[index], (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

        cv2.rectangle(imgOutput, (x - offset, y - offset),
                      (x + w + offset, y + h + offset), (255, 0, 255), 4)

        #cv2.imshow('Imagecrop', imgCrop)
        #cv2.imshow('ImageWhite', imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(30)

# TODO: try except for the hand being outside of the screen
