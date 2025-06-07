import cv2 as cv
import numpy
import win32ui, win32gui
from ctypes import windll
import pyautogui
import threading
import time

NAME_WINDOW = "Path of Exile 2"
BORDER_PIXELS_SIZE = 8
TITLEBAR_PIXELS_SIZE = 30

class WindowCap:
    
    HandleWnd = None
    CaptureIsActive = False
    lock = None
    ScreenWindow = None
    
    def __init__(self):
        self.lock = threading.Lock()
        self.HandleWnd = self.GetWindowHandle()
        self.ScreenWindow = self.GetScreenshot()
        self.start()

    def start(self):
        if self.CaptureIsActive == False:
            self.CaptureIsActive = True
            tCapturing = threading.Thread(target=self.run, daemon=True)
            tCapturing.start()

    def stop(self):
        self.CaptureIsActive = False       
        
    def run(self):
        while True:
            time.sleep(0.1)
            if self.CaptureIsActive == False:
                break
            self.ScreenWindow = self.GetScreenshot()


    def GetWindowHandle(self):
        L_HandleWnd = win32gui.FindWindow(None, NAME_WINDOW)

        if L_HandleWnd:
            return L_HandleWnd
        else:
            print("Окно", NAME_WINDOW, " не найдено")
            return None

    def GetScreenshot(self):
        if not self.HandleWnd is None:  
            EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)
            #print ("EdgesWindow: ", EdgesWindow)
            width = EdgesWindow[2] - EdgesWindow[0]
            height = EdgesWindow[3] - EdgesWindow[1]

            width = width - (BORDER_PIXELS_SIZE * 2)
            height = height - TITLEBAR_PIXELS_SIZE - BORDER_PIXELS_SIZE
            
            
            hwindc = win32gui.GetWindowDC(self.HandleWnd)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            if width >=800:
                bmp.CreateCompatibleBitmap(srcdc, width, height)
                memdc.SelectObject(bmp)

                windll.user32.PrintWindow(self.HandleWnd, memdc.GetSafeHdc(), 3)
                
                signedIntsArray = bmp.GetBitmapBits(True)
                img = numpy.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (height,width,4)

                srcdc.DeleteDC()
                memdc.DeleteDC()
                win32gui.ReleaseDC(self.HandleWnd, hwindc)
                win32gui.DeleteObject(bmp.GetHandle())

                img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)
                cv.imshow("Screen", img)
                return img
            else:
                print("окно свёрнуто или размер окна слишком мал")
        else:          
            self.HandleWnd = self.GetWindowHandle()    
        return None
            

    def winEnumHandler(self, hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

    def PrintAllWindows(self):
        win32gui.EnumWindows( self.winEnumHandler, None )