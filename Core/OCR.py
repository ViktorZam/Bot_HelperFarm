import easyocr
import cv2 as cv
import time
import numpy


reader = easyocr.Reader(["ru"], False)

def GetTextFromImg(img=None):

    img = cv.resize(img, None, fx=2, fy=2, interpolation=cv.INTER_LANCZOS4)
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    
    result = reader.readtext(img, detail=0)

    return result