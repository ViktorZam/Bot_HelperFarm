import easyocr
import cv2 as cv
import time
import numpy


reader = easyocr.Reader(["ru"], False)

def GetTextFromImg(img=None):
    
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    img = cv.resize(img, None, fx=3, fy=3, interpolation=cv.INTER_LANCZOS4)
    
    
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Define the orange color range in HSV
# These values may need adjustment based on the specific shade of orange
    lower_orange = numpy.array([1, 90, 90])
    upper_orange = numpy.array([40, 255, 255])

# Create a mask for the orange color
    mask = cv.inRange(hsv_image, lower_orange, upper_orange)

# Invert the mask to get non-orange regions
    mask_inv = cv.bitwise_not(mask)

# Apply the inverted mask to the original image to remove orange
# This will make the orange areas black
    result_img = cv.bitwise_and(img, img, mask=mask_inv)
    
    cv.imwrite("Debug/" + str(time.time()) + ".png", result_img)
    
    result = reader.readtext(result_img, detail=0, allowlist='0123456789')
    print(result)
    return result