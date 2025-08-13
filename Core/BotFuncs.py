from Core import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum
import math
import numpy
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
    
    def SellItemToTrader(self, special_coord=None):
        L_special_coord = special_coord
        L_AllLocsCharInvSlots = self.TargetManager.GetAllLocsCells(window=Data.EWindow.CHAR_INV_WINDOW, TypeCoord=CalcTarget.ETypeCoord.GLOBAL)
        debug_counter = 0
        loc_item = None
        if L_special_coord:
            debug_coord = L_special_coord
            print("Check cell charInv: ", debug_coord)
            pyautogui.moveTo(L_special_coord[0], L_special_coord[1], 0.2)
            time.sleep(0.2)
            LocObject = self.TargetManager.FindLocObject("Speculate/RareItem.png")
            if not LocObject is None:
                    pyautogui.keyDown("ctrlleft")
                    time.sleep(0.5)
                    pyautogui.click()
                    time.sleep(0.5)
                    pyautogui.keyUp("ctrlleft")
                    loc_item = L_special_coord
            else:
                L_special_coord = None
        
        if L_special_coord is None: 
            for loc in L_AllLocsCharInvSlots:
                debug_counter = debug_counter + 1
                print("Check cell charInv: ", debug_counter)
                pyautogui.moveTo(loc[0], loc[1], 0.1)
                time.sleep(0.2)
                LocObject = self.TargetManager.FindLocObject("Speculate/RareItem.png")
                if not LocObject is None:
                        pyautogui.keyDown("ctrlleft")
                        time.sleep(0.5)
                        pyautogui.click()
                        time.sleep(0.5)
                        pyautogui.keyUp("ctrlleft")
                        loc_item = loc
                        break
                
        return  loc_item

    def OpenCharInv(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/CharInventory.png")
        if LocObject is None:
            pyautogui.press("i")
            time.sleep(1.5)        
         
      
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
        time.sleep(1)    
         
    def EnterFilter(self, filter=CalcTarget.FILTER_RARE_ITEM):
        pyautogui.keyDown("ctrlleft")
        time.sleep(0.5)
        pyautogui.press("f")
        time.sleep(0.5)    
        pyautogui.keyUp("ctrlleft")
        
        time.sleep(0.5)
        clipboard.copy(filter)
        
        pyautogui.keyDown("ctrlleft")
        time.sleep(0.2)
        pyautogui.press("v")
        time.sleep(0.2)    
        pyautogui.keyUp("ctrlleft")
        
        time.sleep(1)
        
    def BuyExpeditionItem(self, item_coord=None, trying=0):
        L_trying = trying
        status_purchased_item = False
        if not item_coord is None:
            self.TargetLoc = item_coord
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
                LocObject = self.TargetManager.FindLocObject("Speculate/BuyExpeditionItem.png")
                self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
                if self.TargetLoc:
                    pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    time.sleep(1)
                    LocObject = self.TargetManager.FindLocObject("Speculate/AcceptBuyingExpeditionItem.png")
                    self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
                    if self.TargetLoc:
                        pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                        time.sleep(0.5)
                        pyautogui.click()
                        time.sleep(1)    
                        status_purchased_item = True
            else:
                if trying < 5:
                    L_trying = L_trying + 1
                    self.BuyExpeditionItem(self.TargetLoc, L_trying)
        return status_purchased_item
    
    def FindRareItemForBuying(self, expedition_window: Data.EWindow, first_coord=None):
        L_AllLocsTraderCells = self.TargetManager.GetAllLocsCells(window=Data.EWindow.EXPEDITION_DEAL_WINDOW, TypeCoord=CalcTarget.ETypeCoord.GLOBAL)
        L_FilterLocs = []
        if expedition_window == Data.EWindow.ROG_WINDOW:
            for column in range(CalcTarget.MAX_COUNT_COLUMN_TRADER_SLOTS):
                if (column % 2) == 1:
                    start_index = (CalcTarget.MAX_COUNT_ROW_TRADER_SLOTS * column) 
                    end_index = ((column + 1) * CalcTarget.MAX_COUNT_ROW_TRADER_SLOTS)
                    L_FilterLocs.extend(L_AllLocsTraderCells[start_index : end_index])
            cache = []
            for index_loc in range(len(L_FilterLocs)):
                if (index_loc % 2) == 1:                 
                    cache.append(L_FilterLocs[index_loc])
            
            L_FilterLocs = cache
        
        index_first_coord = 0
        if first_coord:
           index_first_coord = L_FilterLocs.index(first_coord)
        coord_item = None   
        for loc in L_FilterLocs[index_first_coord:]:
            pyautogui.moveTo(loc[0], loc[1], 0.1)
            time.sleep(0.1)
            print("check item coord: ", loc)
            LocObject = self.TargetManager.FindLocObject("Speculate/RareItem.png")
            if LocObject:
                coord_item = loc
                break   
        
        ##################### Debug BEGIN
        #time.sleep(1)
        #self.TargetManager.WinCapturing.UpdateScreenshot()
        #screen = pyautogui.screenshot()
        #screen = numpy.array(screen)
        #screen = cv.cvtColor(screen, cv.COLOR_RGB2BGR)
        #for loc in L_FilterLocs:    
        #    cv.drawMarker(screen, loc, color=(255,0,255), markerType=cv.MARKER_CROSS)
        #cv.imwrite("Debug/" + str(time.time()) + ".png", screen)
        #################### Debug END
        return coord_item   