import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

def BGR2MeanGreyscale(img):
    """
    Function that will convert a BGR image to a mean valued greyscale image.
    :param img: BGR image that will be converted to greyscale
    :return: The converted greyscale image.
    """

    h, w, = img.shape[:2]
    greyscale_img1 = np.zeros((h, w), np.uint8)
    greyscale_img2 = np.zeros((h, w), np.uint8)
    start_time = time.time()

    for y in range(h):
        for x in range(w):
            I1 = (img.item(y, x, 0) + img.item(y, x, 1) + img.item(y, x, 2))/3
            greyscale_img1.itemset((y, x), I1)
    #print("Execution time for optimized item/itemset function: ","--- %s seconds ---" % (time.time() - start_time))


    """for y in range(h):
        for x in range(w):
            I2 = (int(img[y][x][0]) + int(img[y][x][1]) + int(img[y][x][2]))/3
            greyscale_img2[y][x][0] = I2
    print("Execution time for non optimized function: ", "--- %s seconds ---" % (time.time() - start_time))"""
    return greyscale_img1

def GetDiff(img, spec, TPP, TFP):

    h, w, = img.shape[:2]
    for y in range(h):
        for x in range(w):
            if img.item(y, x) == 255 & spec.item(y, x) == 255:
                TPP += 1
            if img.item(y, x) == 255 & spec.item(y, x) == 0:
                TFP += 1
    return TPP, TFP;