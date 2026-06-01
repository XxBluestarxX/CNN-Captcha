import keras
import cv2
import numpy as np

img_path = 'captcha_03.png'
img = keras.utils.load_img(img_path, target_size=(100, 120), color_mode="grayscale")
img = keras.utils.img_to_array(img)
img = img.astype(np.uint8)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imwrite('img.png',img )