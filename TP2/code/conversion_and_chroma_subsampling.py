# -*- coding: utf-8 -*-
import numpy as np

def convert_pixel_rgb_to_yuv(rgb):
    Y = (rgb[0] + 2*rgb[1] + rgb[2])/4
    U = rgb[2] - rgb[1]
    V = rgb[0] - rgb[1]

    return[Y, U, V]

def convert_pixel_yuv_to_rgb(yuv):
    G = yuv[0] - (yuv[1]+yuv[2])/4
    R = yuv[2] + G
    B = yuv[1] + G

    return [R, G, B]

def convert_image_rgb_to_yuv(image_rgb):
    image_yuv = image_rgb.copy()
    for i in range(len(image_yuv)):
        for j in range(len(image_yuv[i])):
            image_yuv[i][j] = convert_pixel_rgb_to_yuv(image_yuv[i][j])

    return image_yuv

def convert_image_yuv_to_rgb(image_yuv):
    image_rgb = image_yuv.copy()
    for i in range(len(image_rgb)):
        for j in range(len(image_rgb[i])):
            image_rgb[i][j] = convert_pixel_yuv_to_rgb(image_rgb[i][j])

    return image_rgb

# Sous échantillonage de la chrominance 4:2:0
# https://medium.com/@sddkal/chroma-subsampling-in-numpy-47bf2bb5af83
def subsample(img):
    B = img.copy()
    B[1::2, :] = B[::2, :] 
    B[:, 1::2] = B[:, ::2] 

    # Pour garder leur propre luminance
    for i in range(len(img)):
        for j in range(len(img[0])):
            B[i, j][0] = img[i,j][0]

    return B
