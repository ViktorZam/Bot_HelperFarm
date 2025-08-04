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
import clipboard



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
         
    def PickCurrencyFromChest(self, currency_name: Data.ECurrencyName, TypePick: Data.ETypePickCurrency):
        path_img = Data.CURRENCY_IMG_PATH.get(currency_name)[1]
        LocObject = self.TargetManager.FindLocObject(path_img)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.keyDown("ctrlleft")
                time.sleep(0.2)
                if TypePick == Data.ETypePickCurrency.ONE_STACK:
                    pyautogui.click()
                elif TypePick == Data.ETypePickCurrency.ALL:
                    pyautogui.click(button="right")
                time.sleep(0.2)
                pyautogui.keyUp("ctrlleft")
                
                time.sleep(1)
      
      
class Expedition:
      
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        self.TargetManager = TargetManager
    
    def OpenExpeditionWindow(self, window: Data.EWindow):
        
        LocObject = self.TargetManager.FindLocObject(window)
        if not LocObject is None:
            return
        
        char_img_path = Data.ACCORDANCE_WINDOW_AND_CHAR.get(window)
        LocObject = self.TargetManager.FindLocObject(char_img_path, 0.93)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
                LocObject = self.TargetManager.FindLocObject("Speculate/BuySpeachExpedition.png", 0.95)
                if not LocObject is None:
                    self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
                    pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                    time.sleep(0.5)
                    pyautogui.click()       
         
    def EnterFilter(self, filter=CalcTarget.FILTER_RARE_ITEM):
        pyautogui.keyDown("ctrlleft")
        time.sleep(0.2)
        pyautogui.press("f")
        time.sleep(0.2)    
        pyautogui.keyUp("ctrlleft")
        
        time.sleep(0.5)
        clipboard.copy(filter)
        
        pyautogui.keyDown("ctrlleft")
        time.sleep(0.2)
        pyautogui.press("v")
        time.sleep(0.2)    
        pyautogui.keyUp("ctrlleft")