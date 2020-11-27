# -*- coding: utf-8 -*-
import numpy as np

def x_low_pass_filter(img):
    fb_x = (img[:,::2] + img[:,1::2])/2
    return fb_x

def x_high_pass_filter(img):
    fh_x = (img[:,::2] - img[:,1::2])/2 
    return fh_x

def y_low_pass_filter(img):
    fb_y = (img[::2,:] + img[1::2,:])/2
    return fb_y

def y_high_pass_filter(img):
    fh_y = (img[::2,:] - img[1::2,:])/2
    return fh_y

def dwt(n_levels, img):
    im = img.copy()
    result_dwt_image = np.zeros((len(img),len(img[0]), 3))
    for i in range(n_levels):
        if(int(len(im)%2) != 0 or int(len(im[0]/2))%2 != 0):
            n_levels = i
            print("uneven size. number of levels instead: ", n_levels)
            break

        f1 = x_low_pass_filter(im)
        fh = x_high_pass_filter(im)

        f11 = y_low_pass_filter(f1)
        f1h = y_high_pass_filter(f1)
        fh1 = y_low_pass_filter(fh)
        fhh = y_high_pass_filter(fh)

        current_dwt_image = np.concatenate((
            np.concatenate((f11, fh1), axis=1),
            np.concatenate((f1h, fhh), axis=1)),
            axis=0)
        
        result_dwt_image[0:int(len(current_dwt_image)), 0:int(len(current_dwt_image[0]))] = current_dwt_image
        im=f11.copy()


    return n_levels, result_dwt_image



def dwt_inverse_multiple_levels(n_levels, img):
    result_dwt_image = img.copy()
    
    while(n_levels>0):
        n = n_levels - 1
        h = int(len(img))
        w = int(len(img[0]))

        while(n > 0):
            h = int(h/2)
            w = int(w/2)
            n = n - 1

        result_dwt_image[0:h, 0:w] = dwt_inverse_single_level(result_dwt_image[0:h, 0:w])

        n_levels = n_levels - 1

    return result_dwt_image


def dwt_inverse_single_level(img):
    
    f11 = img[0:int(len(img)/2), 0:int(len(img[0])/2)]

    f1_p = np.repeat(f11, 2, axis=0)

    f1 = np.zeros((len(f1_p),int(len(f1_p[0])), 3))
    f1h = img[int(len(img)/2):len(img), 0:int(len(img[0])/2)]

    for i in range(len(f1h)):
        for j in range(len(f1h[0])):
            f1[int(2*i)][j] = f1_p[int(2*i)][j] + f1h[i][j]
            f1[int(2*i+1)][j] = f1_p[int(2*i+1)][j] - f1h[i][j]

    fh1 = img[0:int(len(img)/2), int(len(img[0])/2):int(len(img[0]))]
    fh_p = np.repeat(fh1, 2, axis=0)
    fh = np.zeros((len(fh_p),int(len(fh_p[0])), 3))
    fhh = img[int(len(img)/2):int(len(img)), int(len(img[0])/2):int(len(img[0]))]

    for i in range(len(fhh)):
        for j in range(len(f1h[0])):
            fh[int(2*i)][j] = fh_p[int(2*i)][j] + fhh[i][j]
            fh[int(2*i+1)][j] = fh_p[int(2*i+1)][j] - fhh[i][j]

    f = np.zeros((len(f1),int(len(f1[0])*2), 3))

    for i in range(len(f1)):
        for j in range(len(f1[0])):
            f[i][int(j*2)] = f1[int(i)][j] + fh[i][j]
            f[i][int(j*2+1)] = f1[int(i)][j] - fh[i][j]

    return f