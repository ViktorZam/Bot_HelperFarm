import cv2 as cv
import numpy
import win32ui, win32gui
from ctypes import windll
import pyautogui

NAME_WINDOW = "Path of Exile 2"
BORDER_PIXELS_SIZE = 8
TITLEBAR_PIXELS_SIZE = 30

def GetWindowHandle():
    #try:
    HandleWnd = win32gui.FindWindow(None, NAME_WINDOW)
    #    if not HandleWnd:
    #        raise Exception("Window not found with name: ", NAME_WINDOW)
   # except:
    if HandleWnd:
        return HandleWnd
    else:
        print("Окно", NAME_WINDOW, " не найдено")
        return None

def GetScreenshot():
    HandleWnd = GetWindowHandle()
    if HandleWnd:  
        EdgesWindow = win32gui.GetWindowRect(HandleWnd)
        #print ("EdgesWindow: ", EdgesWindow)
        width = EdgesWindow[2] - EdgesWindow[0]
        height = EdgesWindow[3] - EdgesWindow[1]
        
        #print ("Mouse position: ", pyautogui.position())
        #print ("Window: ", EdgesWindow)
        
        width = width - (BORDER_PIXELS_SIZE * 2)
        height = height - TITLEBAR_PIXELS_SIZE - BORDER_PIXELS_SIZE
        
        
        hwindc = win32gui.GetWindowDC(HandleWnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)

        windll.user32.PrintWindow(HandleWnd, memdc.GetSafeHdc(), 3)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(HandleWnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        #img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)
        return img
    else:
        return None
        

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

def PrintAllWindows():
    win32gui.EnumWindows( winEnumHandler, None )