import cv2
import numpy as np
import os

def read_img():
    img = cv2.imread('captcha_03.png', cv2.IMREAD_GRAYSCALE) # 讀取黑白圖片
    return img

def binary_img(img):
    thresh_value = 128 
    _, binary_image = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY) 
    cv2.imshow('img', binary_image)
    cv2.waitKey(0)
    return binary_image
x = 100
w = 100
y = 120
h = 120
crop_img = read_img()[y:y+h, x:x+w]
cv2.imshow('cropped', crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

def read_posion(img):
    num_labals, labals, stats, _ = cv2.connectedComponentsWithStats(img, connectivity=8)
    components = []
    for i in range(1, num_labals): # '0'為背景 所以從'1'開始
         x, y, w, h, _ = stats[i]
         components.append((x, y, w, h))
    components.sort(key=lambda c:c[0])
    merge_components = []
    current_component = list(components[0])
    print(components)
    for i in range(0,len(components)):
        print(abs(components[i][0] - current_component[0]))
        if abs(components[i][0] - current_component[0]) <= 0:
            current_component[0] = min(current_component[0], components[i][0])
            current_component[1] = min(current_component[1], components[i][1])
            current_component[2] = max(current_component[2], components[i][2])
            current_component[3] = abs(components[i][1] - current_component[1]) + components[i][3]
        else:
            merge_components.append(tuple(current_component[:4]))
            current_component = list(components[i][:4])
    merge_components.append(tuple(current_component[:4]))
    return merge_components

def crop_img(img, x, y, w, h):
    print(cv2.countNonZero(binary_image[y:y+h,x:x+w]))
    if cv2.countNonZero(binary_image[y:y+h,x:x+w]) > 300 : return img[y:y+h, x:x+w]
    else: return 
img = read_img()
binary_image = binary_img(img)
box = read_posion(binary_image)
for i, data in enumerate(box):
    x,y,w,h = data
    print(f'{i}:{x}, {y}, {w}, {h}')
    out = crop_img(binary_image, x, y, w, h)
    try:
        cv2.imwrite(f'cropped_{i}.png', out)
        cv2.imshow('out', out)
        cv2.waitKey(0)
        
    except:
        pass
