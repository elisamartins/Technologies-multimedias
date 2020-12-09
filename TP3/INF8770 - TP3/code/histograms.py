import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct
from skimage import io

def get_image_DC(img):
  imageDC = np.zeros((int(len(img)/8),int(len(img[0])/8)))
  for i in range(0,len(img),8):
    for j in range(0,len(img[0]),8):
        tmp = img[i:i+8,j:j+8]
        tmp = tmp - 128
        resdct = dct(dct(tmp, axis=0, norm='ortho'), axis=1, norm='ortho')
        # On extrait le coefficent DC et on l'ajoute dans une matrice image. 
        imageDC[int(i/8),int(j/8)] = resdct[0,0]/8 + 128

  return imageDC

def get_euclidean_distance(hist1, hist2):
  return np.sqrt(np.sum((hist1-hist2)**2))

def get_edge_histogram(img):
    Gx = cv2.Sobel(img,cv2.CV_8U,1,0, ksize = 5)
    Gy = cv2.Sobel(img,cv2.CV_8U,0,1, ksize = 5)
    angle = np.arctan2(Gx, Gy)
    force_gradient = np.sqrt(np.power(Gx,2)+np.power(Gy,2))
    hist = np.multiply(angle, force_gradient)
    f = np.histogram(hist, bins=100, range=[0, 25])[0]
    return f

def get_color_histogram(img):
  return ([row[0] for row in cv2.calcHist([img], [0], None, [256], [0, 256])] + # Blue 
          [row[0] for row in cv2.calcHist([img], [1], None, [256], [0, 256])] + # Green
          [row[0] for row in cv2.calcHist([img], [2], None, [256], [0, 256])])  # Red