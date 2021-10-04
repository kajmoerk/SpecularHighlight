import cv2 as cv2
import numpy as np
from random import randint
import copy

def RecursiveGrassFire(img, showimg):
    mask = copy.copy(img)
    #kernel = np.ones((2, 2), np.uint8)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #h, w = mask.shape[:2]
    h, w = mask.shape[:2]
    h = h-1
    w = w-1
    save_array = []
    zero_array = []
    blob_array = []
    temp_cord = []
    burnDone = False
    current_ID = 0
    threshold = 30

    for y in range(h):
        for x in range(w):
            if burnDone:
                current_ID = current_ID + 1
                burnDone = False
            if mask[y][x] == 0 and x <= h:
                zero_array.append(mask[y][x])
            elif mask[y][x] == 0 and x >= w:
                zero_array.append(mask[y][x])

    # Looping if x == 1, and some pixels has to be burned
            while mask[y][x] > threshold or len(save_array) > 0:
                mask[y][x] = 0
                temp_cord.append([y, x])
                if mask[y - 1][x] > threshold:
                    if [y - 1, x] not in save_array:
                        save_array.append([y - 1, x])
                if mask[y][x - 1] > threshold:
                    if [y, x - 1] not in save_array:
                        save_array.append([y, x - 1])
                if mask[y + 1][x] > threshold:
                    if [y + 1, x] not in save_array:
                        save_array.append([y + 1, x])
                if mask[y][x + 1] > threshold:
                    if [y, x + 1] not in save_array:
                        save_array.append([y, x + 1])
                if len(save_array)>0:
                    y,x = save_array.pop()

                else:
                    #print("Burn is done")
                    burnDone = True
                    blob_array.append(temp_cord)
                    temp_cord = []
                    break
    maskColor = np.zeros((h,w, 3), np.uint8)
    for blob in range(len(blob_array)):
        B, G, R = randint(0, 255), randint(0, 255), randint(0, 255)
        for cord in blob_array[blob]:
            y,x = cord
            maskColor[y][x][0] = B
            maskColor[y][x][1] = G
            maskColor[y][x][2] = R
    if showimg:
        cv2.imshow("grasfire", maskColor)
        cv2.waitKey(0)
    return maskColor, blob_array
