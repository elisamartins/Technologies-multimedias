# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cv2
from codage_lzw import encode_lzw, getOriginalSize
from conversion_and_chroma_subsampling import convert_image_rgb_to_yuv, convert_image_yuv_to_rgb, subsample
from dwt import dwt, dwt_inverse_multiple_levels, dwt_inverse_single_level
from uniform_deadzone_quantization import deadzone_quantifier, deadzone_dequantifier

IMAGE = "image_noire.jpg"
RECURSION_LEVEL = 3
THRESHOLD = 2
STEP = 1

# Étape 0: Ouverture du fichier image
original_image = (cv2.imread('images/' + IMAGE, cv2.IMREAD_COLOR))
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
original_image = np.array(original_image).astype(np.float)

# Étape 1: Conversion RGB/YUV et chroma subsampling

image_yuv = convert_image_rgb_to_yuv(original_image)
image_yuv_subsampled = subsample(image_yuv)

# Étape 2: Transformée en ondelettes discrètes
n_levels, result_dwt_image = dwt(RECURSION_LEVEL, image_yuv_subsampled)

# # Étape 3: Quantification
q_image = deadzone_quantifier(result_dwt_image, THRESHOLD, STEP)

# Étape 4: Encodage LZW
q_image_1d = q_image.flatten()
compressed_length = encode_lzw(list(map(str, q_image_1d.astype(int))))

# Étape 5: Taux de compression
original_length = getOriginalSize(list(map(str, original_image.flatten().astype(int))))
tc = 1-(compressed_length/original_length)
print("Taux de compression: ", tc)

# Affichage

plt.gcf().canvas.set_window_title('Original Image')
plt.imshow(original_image.astype("uint8"))
plt.show()

#-------------------------------------------------

# Chemin inverse

# Étape 1: Déquantifier
dq_image = deadzone_dequantifier(q_image, THRESHOLD, STEP)

# Étape 2: Transformée inverse
inverse_result_dwt_image = dwt_inverse_multiple_levels(n_levels, dq_image)
# Étape 3: Conversion YUV à RGB
retrieved_image = convert_image_yuv_to_rgb(inverse_result_dwt_image)

# Affichage
plt.gcf().canvas.set_window_title('Retrieved image')
plt.imshow(retrieved_image.astype("uint8"))
plt.show()