import easyocr
import cv2 as cv
import time
import numpy as np


reader = easyocr.Reader(["ru"], False)

def GetTextFromImg(img=None, IncSizeImg=25, thresh=175, filters=True):
    
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    img = cv.resize(img, None, fx=IncSizeImg, fy=IncSizeImg, interpolation=cv.INTER_LANCZOS4)
    if filters:
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]]) #[-1,-1,-1], [-1,9,-1], [-1,-1,-1]#[0,-1,0], [-1,5,-1], [0,-1,0]
        gray_img = cv.filter2D(gray_img, -1, sharpen_kernel)
    
    #binary_img = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 12, 4)
        binary_img = cv.threshold(gray_img,thresh,255,cv.THRESH_BINARY_INV)[1]
        img = binary_img
 

    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    
    result = reader.readtext(img, detail=0, allowlist='0123456789')
    print(result)
    return result