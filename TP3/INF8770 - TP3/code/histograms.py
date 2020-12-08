import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def get_euclidean_distance(hist1, hist2):
  return np.sqrt(np.sum((hist1-hist2)**2))

def get_edge_histogram(img):
    Gx = cv2.Sobel(img,cv2.CV_64F,1,0)
    Gy = cv2.Sobel(img,cv2.CV_64F,0,1)
    angle = np.arctan2(Gx, Gy)
    force_gradient = np.sqrt(np.power(Gx,2)+np.power(Gy,2))
    hist = np.multiply(angle, force_gradient)
    hist=angle
    return np.histogram(np.degrees(hist) % 360.0, bins=360, range=[0, 360])[0]

def get_color_histogram(img):
  return ([row[0] for row in cv2.calcHist([img], [0], None, [256], [0, 256])] + # Blue 
          [row[0] for row in cv2.calcHist([img], [1], None, [256], [0, 256])] + # Green
          [row[0] for row in cv2.calcHist([img], [2], None, [256], [0, 256])])  # Red