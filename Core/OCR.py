import easyocr
import cv2 as cv
import time
import numpy


reader = easyocr.Reader(["ru"], False)

def GetTextFromImg(img=None):
    
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    img = cv.resize(img, None, fx=10, fy=10, interpolation=cv.INTER_LANCZOS4)
 
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    
    result = reader.readtext(img, detail=0, allowlist='0123456789')
    print(result)
    return result