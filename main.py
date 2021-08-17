import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import grassFire as gf
import funcs as f
#img = cv.imread("images/GOPR1656.jpg")
#img = cv.imread("D:/Aalborg Universitet/Aalborg Universitet/P4 - Robotics - General/Projekt/Test_Billeder/Test_(biologers)Torsk_18-05/0326/GOPR1951Cropped.jpg")
img = cv.imread("D:/Aalborg Universitet/Aalborg Universitet/P4 - Robotics - General/Projekt/Torsk_Billeder/1023/P9260034Cropped.jpg")

#imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#H,S,V = cv.split(imgHSV)
#file = V
file = f.BGR2MeanGreyscale(img)


xmin = 1900
xmax = 2010
ymin = 720
ymax = 800
row, col = np.shape(file)
print('Row: ', row)
print('Col: ', col)

sobel_image = np.zeros(shape=(row, col))
Iyy = np.zeros(shape=(row, col))
Ixx = np.zeros(shape=(row, col))

# Define sobel oprator matrix
gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])


for y in range(row - 2):
    for x in range(col - 2):
        I = file.item(y, x)

        if I >= 233:
            Iy = np.sum(np.multiply(gy, file[y:y+3, x:x+3])) # multiply two 3x3 matrix together in y
            Ix = np.sum(np.multiply(gx, file[y:y+3, x:x+3])) # multiply two 3x3 matrix together in x

            Iyy[y, x] = Iy
            Ixx[y, x] = Ix

            sobel_image[y, x] = np.sqrt(Ix**2 + Iy**2)

sobel_imageGrassFire, blobs = gf.RecursiveGrassFire(sobel_image, False)


Test1_Output = np.zeros((row, col), np.uint8)
onlyIntensity = np.zeros((row, col), np.uint8)
sum1 = 0
sum2 = 0
for y in range(row):
    for x in range(col):
        I1 = sobel_image.item(y, x)
        I2 = file.item(y, x)
        if I1 > 30:
            Test1_Output.itemset((y, x), 255)
            sum1 = sum1 + 1
        if I2 >= 250 and Test1_Output.item(y, x,) != 255:
            Test1_Output.itemset((y, x), 255)
            onlyIntensity.itemset((y, x), 255)
            sum1 = sum1 + 1
print(row, col)
print("sum = ", sum1)
print("Normalized sum = ", (sum1/(row*col))*100)

plt.subplot(2,2,1)
plt.title("Billede")
plt.imshow(file, cmap='gray')


plt.subplot(2,2,2)
plt.title("Combined threshold")
plt.imshow(Test1_Output, cmap="gray")


plt.subplot(2,2,3)
plt.title("Only Intensity")
plt.imshow(onlyIntensity, cmap='gray')

#plt.xlim(xmin, xmax)
#plt.ylim(ymin, ymax)

plt.subplot(2,2,4)
plt.title("GrassFire")
plt.imshow(sobel_imageGrassFire, cmap='gray')
plt.show()
