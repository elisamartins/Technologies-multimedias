import numpy as np
import cv2
import math
import csv
from matplotlib import pyplot as plt 

THRESHOLD = 20000

def get_euclidean_distance(hist1, hist2):
  distance = 0
  for j in range(len(hist1)):
    distance += (float(hist1[j]) - float(hist2[j]))**2
  
  return math.sqrt(distance)

def get_color_histogram(img):
  return ([row[0] for row in cv2.calcHist([img], [0], None, [256], [0, 256])] + # Blue 
          [row[0] for row in cv2.calcHist([img], [1], None, [256], [0, 256])] + # Green
          [row[0] for row in cv2.calcHist([img], [2], None, [256], [0, 256])])  # Red

def get_groups(h, groups):
    for el in groups:
            dist = get_euclidean_distance(h, el)
            if(dist< THRESHOLD):
                el = np.multiply(el, 0.75) + np.multiply(h, 0.25)
                return groups
    
    groups.append(np.asarray(h))
    return groups

def get_key_frames(video_number):
    cap = cv2.VideoCapture('../../data/video/v' + str(video_number).zfill(2) + '.mp4')
    groups = []

    frame_number = 0
    while (cap.isOpened()):
      ret, frame = cap.read()
      
      if ret == True:
        h = get_color_histogram(frame)
        frame_number += 1
        print(frame_number)
        groups = get_groups(h, groups)

        if frame_number == 1:
            groups.append(np.asarray(h))

      else:
          break

    print("Number of groups " + str(len(groups)))
    cap.release()

get_key_frames(1)

