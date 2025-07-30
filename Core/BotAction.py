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
import sys
from Core import OCR

class EStateCheckAction(enum.Enum):
    
    DISABLE = 0
    ENABLE = 1


class ActionBase:
    
    HandleWnd = None
    ActionIsActive = False
    lock = None
    TargetLoc = None
    LastTargetLoc = None
    TargetManager = None
    
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        self.TargetManager = TargetManager
        self.lock = threading.Lock()
        self.HandleWnd = self.TargetManager.WinCapturing.HandleWnd
    
    def UpdateTargetLoc(self, Target: tuple[int, int]):
        self.lock.acquire()
        self.TargetLoc = Target
        self.start()
        self.lock.release()
        
    def start(self):
        if self.ActionIsActive == False:
            self.ActionIsActive = True
            tBotAction = threading.Thread(target=self.run, daemon=True)
            tBotAction.start()
    
    def stop(self):
        self.ActionIsActive = False

    def run(self):
        pass

class ActionCheckReady(ActionBase):
    
    CheckingReadyAction = False
    ActionIsReady = False
    Priority = None
    
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        super().__init__(TargetManager)
        self.start_check_ReadyAction()
        
    def start_check_ReadyAction(self):
        if self.CheckingReadyAction == False:
            self.CheckingReadyAction = True
            tCheckingReadyAction = threading.Thread(target=self.run_check_ReadyAction, daemon=True)
            tCheckingReadyAction.start()
    
    def run_check_ReadyAction(self):
        pass
    
    def stop_check_ReadyAction(self):
        self.CheckingReadyAction = False

class ActionFollow(ActionCheckReady):

    RightMouseButton_isDown = False
    Priority = Data.EPriorityAction.MIDDLE

    def run_check_ReadyAction(self):
         while True:
            
            time.sleep(0.5)
            if self.CheckingReadyAction == False:
                break
            
            LocObject = self.TargetManager.FindLocObject("Character.png", 0.8)
            if not LocObject is None:
                self.ActionIsReady = True
            else:
                self.ActionIsReady = False
                self.stop()

    def stop(self):
        super().stop()
        pyautogui.mouseUp(button="Right")
        self.RightMouseButton_isDown = False 
        #print("Hello")      
        
    def run(self):
        while True:
            if self.ActionIsActive == False:
                break
            time.sleep(0.1) #0.1

            LocObject = self.TargetManager.FindLocObject("Character.png", 0.8)
            #print(LocObject)   
            if not LocObject is None:
                self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
                if self.TargetLoc:
                    if self.TargetLoc != self.LastTargetLoc:
                        pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1])
                        #print(self.TargetLoc)
                            
                        if self.RightMouseButton_isDown == False:                     
                            pyautogui.mouseDown(button="Right")
                            #print("123")
                            self.RightMouseButton_isDown = True
                        self.lock.acquire()
                        self.LastTargetLoc = self.TargetLoc
                        self.lock.release() 
                    else:
                        if self.RightMouseButton_isDown == True:
                            pyautogui.mouseUp(button="Right")
                            self.RightMouseButton_isDown = False
                        
class ActionLoot(ActionCheckReady):
    
    Priority = Data.EPriorityAction.HIGHT  
    
    def run_check_ReadyAction(self):
         while True:

            if self.CheckingReadyAction == False:
                break
            LocObject = self.TargetManager.FindLocLootObject()
            #print(LocObject)
            if not LocObject is None:
                self.ActionIsReady = True
            else:
                self.ActionIsReady = False
                self.stop()
            time.sleep(0.5)
            
    def run(self):
        while True:
            if self.ActionIsActive == False:
                break
            
            LocObject = self.TargetManager.FindLocLootObject()
            #print (LocObject)
            if not LocObject is None:
                self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                if self.TargetLoc != self.LastTargetLoc:
                    #print("Local coord Loot: ", self.TargetLoc) 
                    #EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)
                    pyautogui.mouseUp(button="Right")  
                    #pyautogui.moveTo(self.TargetLoc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                    #                self.TargetLoc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)
                    pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1])
                    pyautogui.click()
                    #print(self.TargetLoc)
                    self.lock.acquire()
                    self.LastTargetLoc = self.TargetLoc
                    self.lock.release() 
            time.sleep(1)
            
class ActionSpeculate(ActionBase):
    
    CurrencyImgData = {
        "DIVINE" : "Speculate/Currency/DivineInStock.png",
        "CHAOS" : "Speculate/Currency/ChaosInStock.png",
        "EXALT" : "Speculate/Currency/ExaltInStock.png",
        "ARTIFACT_ORDER" : "Speculate/Currency/ArtifactOrderInStock.png",
        "COINS" : "Speculate/Currency/CoinsInStock.png"   
    }

    CurrencyCountData = {
        "DIVINE" : None,
        "CHAOS" : None,
        "EXALT" : None, 
        "ARTIFACT_ORDER" : None,
        "COINS" : None
    }
    
    CurrencySugTabData = {
        "DIVINE" : Data.ESuggestionTab.CURRENCY,
        "CHAOS" : Data.ESuggestionTab.CURRENCY,
        "EXALT" : Data.ESuggestionTab.CURRENCY, 
        "ARTIFACT_ORDER" : Data.ESuggestionTab.EXPEDITION,
        "COINS" : Data.ESuggestionTab.EXPEDITION
    }
    
    ENOUGH_COUNT_COINS = 100
    ENOUGH_COUNT_ARTIFACT_EXPEDITION = 5 * ENOUGH_COUNT_COINS
    
    Gold = 0
    PrimaryCurrency = sys.argv[1]
    SecondaryCurrency = sys.argv[2] 
    RateCurrencyCache = 1

    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        super().__init__(TargetManager)
        
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1) 

        self.OpenChestTab("Speculate/ExpeditionChestTab.png")
        LocObject = self.TargetManager.FindLocObject("Speculate/ChestWindow.png", 0.97)
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)
        
        LocObject = self.TargetManager.FindLocObject("Speculate/CharInventory.png")
        if LocObject is None:
            pyautogui.press("i")
            time.sleep(1)
            
        #self.PickingAllCurrency()
        
        
        
        #self.CheckEnoughGold()
        
        self.start()
        
    def OpenCurrencyTradeWindow(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            return

        LocObject = self.TargetManager.FindLocObject("Speculate/Alva.png")
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
                LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencySpeach.png", 0.95)
                if not LocObject is None:
                    self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
                    pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                    time.sleep(0.5)
                    pyautogui.click()
    
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
    
    def OpenChestTab(self, path_img_tab):
        self.OpenChest()
        LocObject = self.TargetManager.FindLocObject(path_img_tab)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
    
    def OpenSuggestionTab(self, trying=0, SideSug: Data.ESideSuggestion=Data.ESideSuggestion.HAVE, Tab: Data.ESuggestionTab=Data.ESuggestionTab.IN_STOCK):
        SideSuggestion = SideSug
            
        LocObject = self.TargetManager.FindLocObject(Tab, 0.998)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
        else:
            self.OpenSuggestionWindow(SideSug=SideSuggestion)
            trying = trying + 1
            if trying < 5:
                self.OpenSuggestionTab(trying, SideSug, Tab)
            else:
                return
                
    def OpenSuggestionWindow(self, trying=0, SideSug: Data.ESideSuggestion=Data.ESideSuggestion.HAVE):
        if SideSug == Data.ESideSuggestion.HAVE:
            ButtonSugLoc = CalcTarget.BUTTON_HAVE_LOC
        else:
            ButtonSugLoc = CalcTarget.BUTTON_WANT_LOC
            
        LocObject = self.TargetManager.FindLocObject(SideSug)
        if not LocObject is None:
            return 
        
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None: 
            self.TargetLoc = self.TargetManager.ConvertLocalCoordToGlobal(list(ButtonSugLoc))
            pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(1)
        else:
            self.OpenCurrencyTradeWindow()
            trying = trying + 1
            if trying < 5:
                self.OpenSuggestionWindow(trying, SideSug)
            else:
                return

    def PickingCurrencyFromAlvaTradeWindow(self):
        self.OpenCurrencyTradeWindow()
        L_AllLocsWithdrawn = self.TargetManager.GetAllLocsWithdrawn(CalcTarget.ETypeCoord.GLOBAL)
        for loc in L_AllLocsWithdrawn:
            pyautogui.moveTo(loc[0], loc[1], 0.5)
            time.sleep(1)
            pyautogui.keyDown("ctrlleft")
            time.sleep(0.1)
            pyautogui.click(button="Right")
            time.sleep(0.1)
            pyautogui.keyUp("ctrlleft")
            time.sleep(0.1)
    
    def ClearChest(self):
        self.OpenChest()
        L_AllLocsCharInvSlots = self.TargetManager.GetAllLocsCharInvSlots(CalcTarget.ETypeCoord.GLOBAL)
        debug_counter = 0
        pyautogui.keyDown("ctrlleft")
        for loc in L_AllLocsCharInvSlots:
            pyautogui.moveTo(loc[0], loc[1], 0.2)
            time.sleep(0.2)
            pyautogui.click()
            debug_counter = debug_counter + 1
            print("Click to cell charInv: ", debug_counter)
            
        pyautogui.keyUp("ctrlleft")     

    def MakeScreenWithMask(self, xy_offset_spec_area: tuple, SizeSpecificArea, color_mask=(255,255,255)):
        self.TargetManager.WinCapturing.UpdateScreenshot()
        
        L_ScreenWindowShape = self.TargetManager.WinCapturing.ScreenWindow.shape
        heightScreen = int(L_ScreenWindowShape[0])
        widthScreen = int(L_ScreenWindowShape[1])
        for value in range(1, 5):
            if value == 1:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = int(xy_offset_spec_area[0] - ((SizeSpecificArea/2) + 1))
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 2:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = int(xy_offset_spec_area[1] - ((SizeSpecificArea/2) + 1))
                
            elif value == 3:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = int(xy_offset_spec_area[1] + ((SizeSpecificArea/2) + 1))
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 4:
                X_LT_CoordRectangle = int(xy_offset_spec_area[0] + ((SizeSpecificArea/2) + 1))
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = heightScreen
                
            cv.rectangle(self.TargetManager.WinCapturing.ScreenWindow, (X_LT_CoordRectangle, Y_LT_CoordRectangle), 
                        (X_RD_CoordRectangle, Y_RD_CoordRectangle), color=color_mask, thickness=-1) 
      
    def IsEmptyCharInv(self):
        self.MakeScreenWithMask(xy_offset_spec_area = CalcTarget.XY_OFFSET_FIRST_CHAR_INV_SLOT, 
                                SizeSpecificArea= CalcTarget.SIZE_CHAR_INV_SLOT)
            
        #cv.imwrite("Debug/" + str(time.time()) + ".png", self.TargetManager.WinCapturing.ScreenWindow)    
        LocObject = self.TargetManager.FindLocObject("Speculate/EmptyInvSlot.png", NewScreen=False)
        if not LocObject is None:
            return True
        else:
            return False

    def PickingAllCurrency(self):
        IsTradeCurrencyEmpty = False
        IsEmptyCharInv = False
        
        while (IsTradeCurrencyEmpty and IsEmptyCharInv) != True:
            LocObject = self.TargetManager.FindLocObject("Speculate/TradeComplete.png", 0.52)
            if not LocObject is None:
                self.PickingCurrencyFromAlvaTradeWindow()
            else:
                IsTradeCurrencyEmpty = True

            LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
            if not LocObject is None:
                pyautogui.press("esc")
                time.sleep(1)        
              
            IsEmptyCharInv = self.IsEmptyCharInv()
            
            if (IsEmptyCharInv == False):
                self.ClearChest()
                pyautogui.press("esc") #close chest window
                time.sleep(1)
                IsEmptyCharInv = True
    
    def GetCurrencyFromInStockUI(self, CurrencyName: str):
        path_to_currency = self.CurrencyImgData.get(CurrencyName)
        LocObject = self.TargetManager.FindLocObject(path_to_currency)
        CurrencyValue = None
        LT_Offset = [-5, -10]
        RT_Offset = [0, -10]
        if LocObject:
            LocObject = list(LocObject)
            LT_LocObject = LocObject[0]
            RT_LocObject = LocObject[1]
            LocObject[0] = (LT_LocObject[0] + LT_Offset[0], LT_LocObject[1] + LT_Offset[1])
            LocObject[1] = (RT_LocObject[0] + RT_Offset[0], RT_LocObject[1] + RT_Offset[1])  
            L_CropImg = self.TargetManager.WinCapturing.CropImg(LocObject[0], LocObject[1])
            CurrencyValue = int(OCR.GetTextFromImg(L_CropImg, filters=False, IncSizeImg=25)[0])
        else:
            CurrencyValue = 0 

        return CurrencyValue
    
    def ChangeCountCurrency(self, MathOperation: Data.EMathOperation, CurrencyName: str, Value):
        if MathOperation == Data.EMathOperation.SET:
            L_NewCurrencyCount = Value
        elif MathOperation == Data.EMathOperation.INC:
            if not self.CurrencyCountData.get(CurrencyName) is None:
                L_NewCurrencyCount = self.CurrencyCountData.get(CurrencyName) + Value
            else:
                L_NewCurrencyCount = Value
        elif MathOperation == Data.EMathOperation.DEC:
            if not self.CurrencyCountData.get(CurrencyName) is None:
                L_NewCurrencyCount = self.CurrencyCountData.get(CurrencyName) - Value
            else:
                L_NewCurrencyCount = 0

        self.CurrencyCountData[CurrencyName] = L_NewCurrencyCount
        print(self.CurrencyCountData)    
        
    def UpdateAllCurrencyCountData(self):
        self.OpenSuggestionTab()
        for Currency in list(self.CurrencyCountData.keys()):
            L_CountCurrency = self.GetCurrencyFromInStockUI(Currency)
            self.ChangeCountCurrency(Data.EMathOperation.SET, Currency, L_CountCurrency)
        
        LocObject = self.TargetManager.FindLocObject("Speculate/InStockSugTab.png", 0.998)
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1) 
    
    def SetFieldSuggestion(self, Side: Data.ESideSuggestion, Value):
        self.OpenCurrencyTradeWindow()
        
        if Side == Data.ESideSuggestion.HAVE:
            LocField = CalcTarget.HAVE_FIELD_CENTER_LOC
            LT_LocField = CalcTarget.HAVE_FIELD_LT_LOC
            RT_LocField = CalcTarget.HAVE_FIELD_RT_LOC
        else:
            LocField = CalcTarget.WANT_FIELD_CENTER_LOC
            LT_LocField = CalcTarget.WANT_FIELD_LT_LOC
            RT_LocField = CalcTarget.WANT_FIELD_RT_LOC

        GlobalLocField = self.TargetManager.ConvertLocalCoordToGlobal(LocField)
        pyautogui.moveTo(GlobalLocField[0], GlobalLocField[1], 0.5)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.keyDown("ctrlleft")
        time.sleep(0.2)
        pyautogui.press("a")
        time.sleep(0.2)
        pyautogui.keyUp("ctrlleft")
        time.sleep(0.2)
        pyautogui.press("backspace")
        time.sleep(0.5)
        SetOfValue = str(Value)
        if SetOfValue[0] == "0":
            pyautogui.press("0")
        else:
            for number in SetOfValue:
                pyautogui.press(number)
                time.sleep(0.5)
        
        pyautogui.moveTo(GlobalLocField[0], GlobalLocField[1] + 30, 0.5)
        time.sleep(0.5)
        pyautogui.click()
        
        if Value > 0:
            self.TargetManager.WinCapturing.UpdateScreenshot()
            L_CropImg = self.TargetManager.WinCapturing.CropImg(LT_LocField, RT_LocField)   
            enter_count_currency = int(OCR.GetTextFromImg(L_CropImg, filters=False)[0])
            if enter_count_currency != Value:
                l_side = Side
                l_value = Value
                self.SetFieldSuggestion(l_side, l_value)  
    
    def ConfirmFieldSuggestion(self, Side: Data.ESideSuggestion):
        self.OpenCurrencyTradeWindow()
        
        if Side == Data.ESideSuggestion.HAVE:
            LocField = CalcTarget.HAVE_FIELD_CENTER_LOC
        else:
            LocField = CalcTarget.WANT_FIELD_CENTER_LOC

        GlobalLocField = self.TargetManager.ConvertLocalCoordToGlobal(LocField)
        pyautogui.moveTo(GlobalLocField[0], GlobalLocField[1], 0.5)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.moveTo(GlobalLocField[0], GlobalLocField[1] + 30, 0.5)
        time.sleep(0.5)
        pyautogui.click()
    
    def SetCurrencyForSuggestion(self, Side: Data.ESideSuggestion, CurrencyName):
        self.OpenCurrencyTradeWindow()
        if Side == Data.ESideSuggestion.HAVE:
            self.OpenSuggestionTab(SideSug=Side, Tab=Data.ESuggestionTab.IN_STOCK)
        else:
            sug_tab = self.CurrencySugTabData.get(CurrencyName)
            self.OpenSuggestionTab(SideSug=Side, Tab=sug_tab)
        
        path_to_currency = self.CurrencyImgData.get(CurrencyName)
        LocObject = self.TargetManager.FindLocObject(path_to_currency)
        if LocObject:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
    
    def UpdateRateCurrencyCache(self, have_slot_currency_name, want_slot_currency_name):
        self.SetCurrencyForSuggestion(Data.ESideSuggestion.HAVE, have_slot_currency_name)    
        self.SetCurrencyForSuggestion(Data.ESideSuggestion.WANT, want_slot_currency_name)
        L_GlobalZeroCoord = self.TargetManager.ConvertLocalCoordToGlobal([0, 0])
        pyautogui.moveTo(L_GlobalZeroCoord[0], L_GlobalZeroCoord[1], 1)
        time.sleep(1)    
        self.TargetManager.WinCapturing.UpdateScreenshot()
        L_CropImg = self.TargetManager.WinCapturing.CropImg(CalcTarget.CURRENT_CURRENCY_RATE_LT_LOC, CalcTarget.CURRENT_CURRENCY_RATE_RT_LOC)   
        rate_currency = OCR.GetTextFromImg(L_CropImg, filters=False, allowchars=OCR.RATE_CURRENCY_ALLOW_LIST)
        self.RateCurrencyCache = OCR.RateStringToNumbers(rate_currency)[0]
    
    def UpdateCountGold(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/CharInventory.png", 0.95)
        if LocObject is None:
            pyautogui.press("i")
        
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)
        
        self.TargetManager.WinCapturing.UpdateScreenshot()
        L_CropImg = self.TargetManager.WinCapturing.CropImg(CalcTarget.GOLD_LT_LOC, CalcTarget.GOLD_RT_LOC)   
        self.Gold = int(OCR.GetTextFromImg(L_CropImg, filters=False)[0])
        return self.Gold
    
    def PlaceLot(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if LocObject is None:
            self.OpenCurrencyTradeWindow()

        LocObject = self.TargetManager.FindLocObject("Speculate/PlaceLot.png")
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
    
    def BuyCurrency(self, have_currency_name, have_currency_count=None, want_currency_name=None, want_currency_count=None):
        L_have_currency_count = have_currency_count
        L_want_currency_count = want_currency_count
        
        self.UpdateRateCurrencyCache(have_currency_name, want_currency_name)
        is_want_confirm_currency = True
        
        self.RateCurrencyCache
        if L_want_currency_count is None:
                is_want_confirm_currency = True 
           
        elif L_have_currency_count is None:
            if self.RateCurrencyCache > want_currency_count:
                is_want_confirm_currency = True
                L_have_currency_count = 1
            else:
                is_want_confirm_currency = False    
             
        if is_want_confirm_currency:
            self.SetFieldSuggestion(Data.ESideSuggestion.HAVE, L_have_currency_count)
            self.SetFieldSuggestion(Data.ESideSuggestion.WANT, 0) 
            self.ConfirmFieldSuggestion(Data.ESideSuggestion.WANT)
        else:
            self.SetFieldSuggestion(Data.ESideSuggestion.WANT, L_want_currency_count)
            self.SetFieldSuggestion(Data.ESideSuggestion.HAVE, 0) 
            self.ConfirmFieldSuggestion(Data.ESideSuggestion.HAVE)
        
        self.PlaceLot()   
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)   
        DealIsNotComplete = True
        while DealIsNotComplete:
            LocObject = self.TargetManager.FindLocObject("Speculate/TradeComplete.png", 0.52)
            if not LocObject is None:
                DealIsNotComplete = False
                
            time.sleep(3)
        self.PickingAllCurrency()
        return 
       
    def CheckEnoughGold(self):
        self.UpdateCountGold() 
        self.UpdateRateCurrencyCache(self.PrimaryCurrency, self.SecondaryCurrency)
        self.SetFieldSuggestion(Data.ESideSuggestion.HAVE, 1)
        self.SetFieldSuggestion(Data.ESideSuggestion.WANT, 0)
        self.ConfirmFieldSuggestion(Data.ESideSuggestion.WANT)
        self.TargetManager.WinCapturing.UpdateScreenshot()
        L_CropImg = self.TargetManager.WinCapturing.CropImg(CalcTarget.COST_TRADE_CENTER_LT_LOC, CalcTarget.COST_TRADE_CENTER_RT_LOC)   
        cost_deal = int(OCR.GetTextFromImg(L_CropImg, filters=False)[0])
        count_primary_currency = self.CurrencyCountData.get(self.PrimaryCurrency)
        RequiredAmountGoldForDeal = cost_deal * count_primary_currency
        print(RequiredAmountGoldForDeal)
    
    def FillStockExpeditionCurrency(self):
        
        ExpeditionCurrencies = ("COINS", "ARTIFACT_ORDER")
        for expedition_currency_name in ExpeditionCurrencies:
            if expedition_currency_name == "COINS":
                enough_count_expedition_currency = self.ENOUGH_COUNT_COINS
            else:
                enough_count_expedition_currency = self.ENOUGH_COUNT_ARTIFACT_EXPEDITION
        
            if self.CurrencyCountData.get(expedition_currency_name) < enough_count_expedition_currency:
                RequiredAmountCurrency = enough_count_expedition_currency - self.CurrencyCountData.get(expedition_currency_name)
                self.UpdateRateCurrencyCache("EXALT", expedition_currency_name)
            
                if self.RateCurrencyCache >= RequiredAmountCurrency:
                    if self.CurrencyCountData.get("EXALT") < 1:
                        self.BuyCurrency("CHAOS", have_currency_count=1, want_currency_name="EXALT")
                        
                    self.BuyCurrency("EXALT", 1, want_currency_name=expedition_currency_name)
                    
                else:    
                    RequiredCountExalt = math.ceil(RequiredAmountCurrency / self.RateCurrencyCache)
                    if self.CurrencyCountData.get("EXALT") < RequiredCountExalt:
                        self.BuyCurrency("CHAOS", want_currency_name="EXALT", want_currency_count=RequiredCountExalt)
                    
                    self.BuyCurrency("EXALT", RequiredCountExalt, want_currency_name=expedition_currency_name)
                
           
    def run(self):
        while True:
            if self.ActionIsActive == False:
                break
            

            self.UpdateAllCurrencyCountData()               
            self.FillStockExpeditionCurrency()
            time.sleep(2)
            
            ##################### Debug BEGIN
            EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)
            EdgesWindow = list(EdgesWindow)
            EdgesWindow[0] = EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE
            EdgesWindow[1] = EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE 
            print("Left pos win: ", EdgesWindow)
            print("mouse pos: ", pyautogui.position())
            #################### Debug END
            
    def rrr(self):
        pass
    