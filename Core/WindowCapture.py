import cv2 as cv
import numpy
import win32ui, win32gui
from ctypes import windll
import pyautogui
import threading
import time
from Core import Debug
import enum

NAME_WINDOW = "Path of Exile 2"
BORDER_PIXELS_SIZE = 8
TITLEBAR_PIXELS_SIZE = 31

class ETypeScreening(enum.Enum):
    
    AUTO = 0
    MANUAL = 1


class WindowCap:
    
    HandleWnd = None
    CaptureIsActive = False
    lock = None
    ScreenWindow = None
    LT_ObjectLoc = None
    RD_ObjectLoc = None
    TargetLoc = None
    TypeScreening = None
    
    def __init__(self, TypeScreening: ETypeScreening = ETypeScreening.AUTO):
        self.lock = threading.Lock()
        self.HandleWnd = self.GetWindowHandle()
        self.ScreenWindow = self.GetScreenshot()
        self.TypeScreening = TypeScreening
        if (self.TypeScreening == ETypeScreening.AUTO):
            self.start()

    def start(self):
        if self.CaptureIsActive == False:
            self.CaptureIsActive = True
            tCapturing = threading.Thread(target=self.run, daemon=True)
            tCapturing.start()

    def stop(self):
        self.CaptureIsActive = False       
    
    def SetDebugLocs(self, LT_ObjectLoc, RD_ObjectLoc, TargetLoc):
        self.LT_ObjectLoc = LT_ObjectLoc
        self.RD_ObjectLoc = RD_ObjectLoc
        self.TargetLoc = TargetLoc
        
    def run(self):
        while True:
            time.sleep(0.1) #0.1
            if self.CaptureIsActive == False:
                break
            self.UpdateScreenshot()
            if Debug.DEBUG_MODE == Debug.EDebugMode.DEBUG_MODE_ON:
                L_ScreenWindow = self.ScreenWindow
                cv.rectangle(L_ScreenWindow, self.LT_ObjectLoc, self.RD_ObjectLoc, color=(0,255,0), thickness=2, lineType=cv.LINE_4)     
                cv.drawMarker(L_ScreenWindow, self.TargetLoc, color=(255,0,255), markerType=cv.MARKER_CROSS)
                #cv.imshow("Screen", L_ScreenWindow)
                cv.imwrite("Debug/" + str(time.time()) + ".png", L_ScreenWindow)
                #cv.waitKey(1) 
    
    def UpdateScreenshot(self):
        self.lock.acquire()
        self.ScreenWindow = self.GetScreenshot()
        self.lock.release()
        time.sleep(0.1)
        return self.ScreenWindow                

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
            if not srcdc is None:
                memdc = srcdc.CreateCompatibleDC()
                bmp = win32ui.CreateBitmap()
                if width >=800:
                    #print(bmp, "///", width, "///", height)
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
                    return img
                else:
                    print("окно свёрнуто или размер окна слишком мал")
                    time.sleep(2)
            else:
                self.lock.acquire()
                self.HandleWnd = self.GetWindowHandle()
                self.lock.release()          
                
        return None
            
    def CropImg(self, LTPos, RTPos):
        self.lock.acquire()
        self.ScreenWindow = self.ScreenWindow[LTPos[1]:RTPos[1], LTPos[0]:RTPos[0]]
        self.lock.release()
        #cv.imwrite("Debug/" + str(time.time()) + ".png", self.ScreenWindow)
        return self.ScreenWindow
        
    def winEnumHandler(self, hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

    def PrintAllWindows(self):
        win32gui.EnumWindows( self.winEnumHandler, None )