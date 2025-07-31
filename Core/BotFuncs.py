from Core import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum
import math
from Core import Data
from Core import CalcTarget
import cv2 as cv
from Core import OCR


class General:
    
    TargetManager = None
    
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        self.TargetManager = TargetManager

    def CloseWindow(self, window: Data.EWindow):
        Accuracy_equal = Data.WINDOW_ACCURACY_EQUAL_DATA.get(window)
        LocObject = self.TargetManager.FindLocObject(window, Accuracy_equal)
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)
    
    def OpenChest(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/ChestWindow.png", 0.97)
        if not LocObject is None:
            return
        
        LocObject = self.TargetManager.FindLocObject("Speculate/Chest.png")
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
    
    def OpenChestTab(self, path_img_tab: Data.ETab):
        self.OpenChest()
        LocObject = self.TargetManager.FindLocObject(path_img_tab)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
         
      
class Expedition:
      
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        self.TargetManager = TargetManager
             
         
            
