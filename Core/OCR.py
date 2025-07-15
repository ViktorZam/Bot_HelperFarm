import easyocr
import cv2 as cv
import time
import numpy


reader = easyocr.Reader(["ru"], False)

def GetTextFromImg(img=None):
    
    
    NewImage = img
    #NewImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    #NewImage = cv.equalizeHist(NewImage)

    #NewImage = cv.GaussianBlur(NewImage, (5, 5), 1)
    
    
    cv.imwrite("Debug/" + str(time.time()) + ".png", NewImage)
    #cv.imwrite("Debug/" + "123" + ".png", img)

    result = reader.readtext(NewImage, detail=0)

    return result