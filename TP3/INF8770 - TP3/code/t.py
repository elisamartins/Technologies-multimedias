
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import math

"""Lecture de l'image en tons de gris et affichage. Le calcul des gradients sur une image est toujours sur l'image d'intensité."""

image_name = '../../data/png/i010.png'

image = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
plt.figure(figsize = (10,10))
plt.imshow(image,cmap = plt.get_cmap('gray'))
plt.show()

height = len(image)
width = len(image[0])

"""Pour faire la convolution avec un filtre de Sobel, il faut ajouter des lignes et colonnes additionnelles pour permettre les calculs aux frontières. Ici, on duplique les valeurs des frontières."""

col=image[:,0]
image = np.column_stack((col,image))
col=image[:,len(image[0])-1]
image = np.column_stack((image,col))
row=image[0,:]
image = np.row_stack((row,image))
row=image[len(image)-1,:]
image = np.row_stack((image,row))

"""Calcul de la convolution avec les filtres de Sobel selon l'axe X et l'axe Y. On peut faire la convolution aussi avec cv2.sobel(). Le calcul sera plus rapide."""

Gx = np.zeros((height,width), 'float')
Gy = np.zeros((height,width), 'float')
#Filtres Sobel
Sobelx= [[-1.0,0.0,1.0],[-2.0,0.0,2.0],[-1.0,0.0,1.0]]
Sobely= [[-1.0,-2.0,-1.0],[0.0,0.0,0.0],[1.0,2.0,1.0]]
for row in range(1,len(image)-1):
    for col in range(1,len(image[row])-1):
        for i in range(-1,2):
            for j in range(-1,2):
                #Convolutions. On calcule en X et Y simultanément. 
                Gx[row-1][col-1] += np.multiply(Sobelx[i+1][j+1],image[row-i][col-j])
                Gy[row-1][col-1] += np.multiply(Sobely[i+1][j+1],image[row-i][col-j])

angle = np.arctan2(Gx, Gy)
print(angle)
plt.figure(figsize = (10,10))
plt.imshow(angle,cmap = plt.get_cmap('binary'))
plt.show()

# """Les gradients peuvent être positifs ou négatifs. Pour l'affichage, on fait la valeur absolue et on normalise les valeurs entre 0 et 255. Affichage pour l'axe X. On détecte bien les lignes verticales, mais pas très bien les lignes horizontales."""

# Gxout =  np.absolute(Gx)
# Gxout = Gxout * 255/np.max(Gxout)
# plt.figure(figsize = (10,10))
# plt.imshow(Gxout,cmap = plt.get_cmap('binary'))
# plt.show()

# """Affichage pour l'axe Y. On détecte bien les lignes horizontales. La combinaison des 2 filtres permet de bien détecter les diagonales. """

# Gyout =  np.absolute(Gy)
# Gyout = Gyout * 255/np.max(Gyout)
# plt.figure(figsize = (10,10))
# plt.imshow(Gyout,cmap = plt.get_cmap('binary'))
# plt.show()

# """Affichage des matrices de gradients. Il y a des valeurs réelles positives et négatives."""

# print("Gx:", Gx)
# print("Gy:", Gy)

# """Extraction d'arêtes à partir des gradients. On calcule la force des gradients, et ensuite on seuille la force des gradients calculée."""

# ForceGradient = np.sqrt(np.power(Gx,2)+np.power(Gy,2))

# """Gradients plus fort que 80. """

# aretes = ForceGradient>80
# plt.figure(figsize = (10,10))
# plt.imshow(aretes, plt.get_cmap('binary'))
# plt.show()

# """Gradients plus fort que 150. Le seuillage permet d'obtenir différents niveaux de détails. """

# aretes = ForceGradient>150
# plt.figure(figsize = (10,10))
# plt.imshow(aretes, plt.get_cmap('binary'))
# plt.show()

