# -*- coding: utf-8 -*-
import numpy as np
import math

def real_value(val):
    return 255 - val

def quantify_pixel_comp(threshold, step, pixel_comp):
    if pixel_comp > threshold and pixel_comp >= 0:
           return math.ceil((pixel_comp-threshold)/step)
    elif pixel_comp < 0:
        if(real_value(pixel_comp) >  threshold):
            return math.ceil((pixel_comp-threshold)/step)
    return 0

def deadzone_quantifier(img, threshold, step):
    quantified = np.zeros((len(img),len(img[0]), 3))
    for i in range(len(img)):
        for j in range(len(img[0])):

            quantified[i][j][0] = quantify_pixel_comp(threshold, step, img[i][j][0])
            quantified[i][j][1] = quantify_pixel_comp(threshold, step, img[i][j][1])
            quantified[i][j][2] = quantify_pixel_comp(threshold, step, img[i][j][2])
       
    return quantified

def dequantify_pixel_comp(threshold, step, pixel_comp):
    if(pixel_comp == 0):
        return 0
    
    return math.ceil((pixel_comp+threshold)*step)

def deadzone_dequantifier(img, threshold, step):
    dequantified = np.zeros((len(img),len(img[0]), 3))
    for i in range(len(img)):
        for j in range(len(img[0])):

            dequantified[i][j][0] = dequantify_pixel_comp(threshold, step, img[i][j][0])
            dequantified[i][j][1] = dequantify_pixel_comp(threshold, step, img[i][j][1])
            dequantified[i][j][2] = dequantify_pixel_comp(threshold, step, img[i][j][2])
       
    return dequantified
