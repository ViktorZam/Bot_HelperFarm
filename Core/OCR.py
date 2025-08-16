import easyocr
import cv2 as cv
import time
import numpy as np

reader = easyocr.Reader(["ru"], False, 
                        model_storage_directory="EasyOCR/model",
                        user_network_directory="EasyOCR/user_network",
                        recog_network='custom_model')
CURRENCY_ALLOW_LIST = '0123456789'
RATE_CURRENCY_ALLOW_LIST = '0123456789.,:'


def GetTextFromImg(img=None, IncSizeImg=25, thresh=175, filters=True, allowchars=CURRENCY_ALLOW_LIST, check_paragraph=False):
    
    #cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    img = cv.resize(img, None, fx=IncSizeImg, fy=IncSizeImg, interpolation=cv.INTER_LANCZOS4)#cv.INTER_LANCZOS4
    if filters:
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]]) #[-1,-1,-1], [-1,9,-1], [-1,-1,-1]#[0,-1,0], [-1,5,-1], [0,-1,0]
        gray_img = cv.filter2D(gray_img, -1, sharpen_kernel)
    
    #binary_img = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 12, 4)
        binary_img = cv.threshold(gray_img,thresh,255,cv.THRESH_BINARY_INV)[1]
        img = binary_img
 

    cv.imwrite("Debug/" + str(time.time()) + ".png", img)
    
    result = reader.readtext(img, detail=0, allowlist=allowchars, paragraph=check_paragraph)
    print(result)
    return result

def RateStringToNumbers(ocr_string):
    chars = ""
    chars = chars.join(ocr_string)
    chars = list(chars)
    number_string = ""
    numbers = []
    for char in chars:
        if char != ":":
            number_string = number_string + char
            chars.count
        else:
            number_string = float(number_string)
            if (number_string % 1) == 0:
                number_string = int(number_string)

            numbers.append(number_string)
            number_string = ""
     
    number_string = float(number_string)
    if (number_string % 1) == 0:
        number_string = int(number_string) 
            
    numbers.append(number_string)
    return numbers
