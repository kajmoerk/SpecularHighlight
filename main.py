import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import grassFire as gf
import funcs as f
import glob
images = glob.glob("images/Original/*")
specv = glob.glob("images/specv5/*")


Totalsum = 0
TPP = 0
TFP = 0
counter = 0
for i in range(len(images)): #Running the loop dee loop
    img = cv.imread(images[i])
    img_specv = cv.imread(specv[i])
    file = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    file_specv = cv.cvtColor(img_specv, cv.COLOR_BGR2GRAY)
    xmin = 1900
    xmax = 2010
    ymin = 720
    ymax = 800
    row, col = np.shape(file)
    #print('Row: ', row)
    #print('Col: ', col)

    sobel_image = np.zeros(shape=(row, col))
    Iyy = np.zeros(shape=(row, col))
    Ixx = np.zeros(shape=(row, col))

    # Define sobel oprator matrix
    gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
    gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])


    for y in range(row - 2): # Edge detection
        for x in range(col - 2):
            I = file.item(y, x)

            if I >= 250: #Orig = I >= 233
                Iy = np.sum(np.multiply(gy, file[y:y+3, x:x+3])) # multiply two 3x3 matrix together in y
                Ix = np.sum(np.multiply(gx, file[y:y+3, x:x+3])) # multiply two 3x3 matrix together in x

                Iyy[y, x] = Iy
                Ixx[y, x] = Ix

                sobel_image[y, x] = np.sqrt(Ix**2 + Iy**2)

    #sobel_imageGrassFire, blobs = gf.RecursiveGrassFire(sobel_image, False)

    Test1_Output = np.zeros((row, col), np.uint8)
    onlyIntensity = np.zeros((row, col), np.uint8)
    sum1 = 0
    sum2 = 0
    for y in range(row):
        for x in range(col):
            I1 = sobel_image.item(y, x)
            I2 = file.item(y, x)
            if I1 > 30: #Orig = I1 > 30
                Test1_Output.itemset((y, x), 255)
                sum1 = sum1 + 1
            if I2 >= 245 and Test1_Output.item(y, x,) != 255: #Orig = I2 >= 245
                Test1_Output.itemset((y, x), 255)
                onlyIntensity.itemset((y, x), 255)
                sum1 = sum1 + 1
    kernel1 = np.ones((1, 1), np.uint8)
    kernel2 = np.ones((3, 3), np.uint8)
    #Test1_Output = cv.morphologyEx(Test1_Output, cv.MORPH_ERODE, kernel1)
    #Test1_Output = cv.morphologyEx(Test1_Output, cv.MORPH_ERODE, kernel1)
    Test1_Output = cv.morphologyEx(Test1_Output, cv.MORPH_DILATE, kernel2)
    TPP, TFP, counter = f.GetDiff(Test1_Output, file_specv, TPP, TFP, counter)
    print("TPP = ",TPP, " TFP = ", TFP, "Total specular highlight pixels = ", counter)
    #print("sum = ", sum1)
    print(images[i])
    print(specv[i])

    """plt.subplot(2, 1, 1)
    plt.title("Ours")
    plt.imshow(Test1_Output, cmap='gray')

    plt.subplot(2, 1, 2)
    plt.title("Kontrol")
    plt.imshow(file_specv, cmap="gray")
    plt.show()"""
    #print("Normalized sum = ", (sum1/(row*col))*100)


"""""
# Show all the individual images.

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
"""""