import numpy as np
import cv2
import math
import csv
from matplotlib import pyplot as plt 

def get_euclidean_distance(hist1, hist2):
  distance = 0
  for j in range(len(hist1)):
    distance += (float(hist1[j]) - float(hist2[j]))**2
  
  return math.sqrt(distance)

def get_color_histogram(img):
  b = [row[0] for row in cv2.calcHist([img], [0], None, [256], [0, 256])]
  g = [row[0] for row in cv2.calcHist([img], [1], None, [256], [0, 256])]
  r = [row[0] for row in cv2.calcHist([img], [2], None, [256], [0, 256])]

  return b+g+r

def get_video(image):
  img_hist = get_color_histogram(image)
  smallest_dist = 99999999
  video_number = 1
  for i in range(1, 51):
      f = open('../data/color_histograms/' + str(i) + '.csv', 'r')
      f_reader = csv.reader(f, delimiter=',')
      for row in f_reader:
        current_dist = get_euclidean_distance(row, img_hist)
        if current_dist < smallest_dist:
          smallest_dist = current_dist
          video_number = i
  return video_number

def generate_indexation_file(video_number):
  f_writer = csv.writer(open('../data/color_histograms/' + str(video_number) + '.csv', 'w', newline=''))
  cap = cv2.VideoCapture('../data/video/v' + str(video_number).zfill(2) + '.mp4')

  frame_number = 0
  current_frame = None

  while (cap.isOpened()):
      ret, frame = cap.read()
      
      if ret == True:
          frame_number += 1
          if frame_number % 30 == 0:
            f_writer.writerow(get_color_histogram(frame))

      else:
          break

  cap.release()
  
def generate_indexation_files():
  for i in range(1, 51):
    generate_indexation_file(i)

def get_solution():
  f_writer = csv.writer(open('../data/carol_solution.csv', 'w', newline=''))

  for i in range(1, 201):
    result = get_video(cv2.imread('../data/png/i' + str(i).zfill(3) + '.png', cv2.IMREAD_COLOR))
    f_writer.writerow([i, result])

#generate_indexation_files()
get_solution()