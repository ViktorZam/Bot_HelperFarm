from Core import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum
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
        "DIVINE" : ("Speculate/Currency/DivineLot.png", "Speculate/Currency/DivineInStock.png"),
        "CHAOS" : ("Speculate/Currency/ChaosLot.png", "Speculate/Currency/ChaosInStock.png"),
        "EXALT" : ("Speculate/Currency/ExaltLot.png", "Speculate/Currency/ExaltInStock.png"),
        "ARTIFACT_ORDER" : ("Speculate/Currency/ArtifactOrderLot.png", "Speculate/Currency/ArtifactOrderInStock.png"),
        "COINS" : ("Speculate/Currency/CoinsLot.png", "Speculate/Currency/CoinsInStock.png")   
    }

    CurrencyCountData = {
        "DIVINE" : None,
        "CHAOS" : None,
        "EXALT" : None, 
        "ARTIFACT_ORDER" : None,
        "COINS" : None
    }
    
    CurrencyCropOffsetTradeUI = {
        "DIVINE" : (13, 11, 0, 19),
        "CHAOS" : (8, 13, 0, 14),
        "EXALT" : (5, 11, 0, 10), 
        "ARTIFACT_ORDER" : (12, 12, 0, 8),
        "COINS" : (8, 14, 0, 14)
    }
    

    Gold = 0
    PrimaryCurrency = sys.argv[1]
    SecondaryCurrency = sys.argv[2] 

    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        super().__init__(TargetManager)
        
        self.OpenChestTab("Speculate/ExpeditionChestTab.png")
        LocObject = self.TargetManager.FindLocObject("Speculate/ChestWindow.png", 0.97)
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)
        
        LocObject = self.TargetManager.FindLocObject("Speculate/CharInventory.png", 0.95)
        if LocObject is None:
            pyautogui.press("i")
            
        #self.SetFieldSuggestion(Data.ESideSuggestion.WANT, 0)
            
            
            
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1) 

        
        #self.PickingAllCurrency()
        
        #self.UpdateAllCurrencyCountData()
        
            
        self.start()
        
    def OpenCurrencyTradeWindow(self):
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            return

        LocObject = self.TargetManager.FindLocObject("Speculate/Alva.png", 0.95)
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
    
    def OpenTradeInStockTab(self, trying=0):
        LocObject = self.TargetManager.FindLocObject("Speculate/InStock.png", 1)
        if not LocObject is None:
            return
        
        LocObject = self.TargetManager.FindLocObject("Speculate/InStock.png", 0.998)
        if not LocObject is None:
            self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
                time.sleep(0.5)
                pyautogui.click()
                time.sleep(1)
        else:
            self.OpenTradeHaveWindow()
            trying = trying + 1
            if trying < 5:
                self.OpenTradeInStockTab(trying)
            else:
                return
                
    def OpenTradeHaveWindow(self, trying=0):
        LocObject = self.TargetManager.FindLocObject("Speculate/InStock.png", 0.998)
        if not LocObject is None:
            return 
        
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None: 
            self.TargetLoc = self.TargetManager.ConvertLocalCoordToGlobal(list(CalcTarget.BUTTON_HAVE_LOC))
            pyautogui.moveTo(self.TargetLoc[0], self.TargetLoc[1], 0.5)
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(1)
        else:
            self.OpenCurrencyTradeWindow()
            trying = trying + 1
            if trying < 5:
                self.OpenTradeHaveWindow(trying)
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
        pyautogui.keyDown("ctrlleft")
        for loc in L_AllLocsCharInvSlots:
            pyautogui.moveTo(loc[0], loc[1], 0.2)
            time.sleep(0.2)
            pyautogui.click()
            
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
                X_RD_CoordRectangle = int(xy_offset_spec_area[0] - ((SizeSpecificArea/2) + 5))
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 2:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = int(xy_offset_spec_area[1] - ((SizeSpecificArea/2) + 5))
                
            elif value == 3:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = int(xy_offset_spec_area[1] + ((SizeSpecificArea/2) + 5))
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 4:
                X_LT_CoordRectangle = int(xy_offset_spec_area[0] + ((SizeSpecificArea/2) + 5))
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
        
        while (IsTradeCurrencyEmpty and IsEmptyCharInv) == True:
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
        path_to_currency = self.CurrencyImgData.get(CurrencyName)[1]
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
            CurrencyValue = int(OCR.GetTextFromImg(L_CropImg, IncSizeImg=25)[0])
        else:
            CurrencyValue = 0 

        return CurrencyValue
      
    def GetCountCurrencyFromCurrencyTradeUI(self, CurrencyName: str, Accuracy=0.94, UpdateScreen=True):
        LT_X_offset = self.CurrencyCropOffsetTradeUI.get(CurrencyName)[0]
        LT_Y_offset = self.CurrencyCropOffsetTradeUI.get(CurrencyName)[1]
        RT_X_offset = self.CurrencyCropOffsetTradeUI.get(CurrencyName)[2]
        RT_Y_offset = self.CurrencyCropOffsetTradeUI.get(CurrencyName)[3]
        path_to_currency = self.CurrencyImgData.get(CurrencyName)[0]
            
        LocObject = self.TargetManager.FindLocObject(path_to_currency, Accuracy, NewScreen=UpdateScreen)
        CurrencyValue = None
        if LocObject:
            LocObject = list(LocObject)
            LT_LocObject = LocObject[0]
            RT_LocObject = LocObject[1]
            LocObject[0] = (LT_LocObject[0] - LT_X_offset, LT_LocObject[1] - LT_Y_offset)
            LocObject[1] = (RT_LocObject[0] - RT_X_offset, RT_LocObject[1] - RT_Y_offset)
            L_CropImg = self.TargetManager.WinCapturing.CropImg(LocObject[0], LocObject[1])
            CurrencyValue = int(OCR.GetTextFromImg(L_CropImg, filters=False)[0]) 

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
        self.OpenTradeInStockTab()
        for Currency in list(self.CurrencyCountData.keys()):
            L_CountCurrency = self.GetCurrencyFromInStockUI(Currency)
            self.ChangeCountCurrency(Data.EMathOperation.INC, Currency, L_CountCurrency)
        
        LocObject = self.TargetManager.FindLocObject("Speculate/InStock.png", 0.998)
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1) 
        
        self.OpenCurrencyTradeWindow()
        L_GlobalZeroCoord = self.TargetManager.ConvertLocalCoordToGlobal([0, 0])
        pyautogui.moveTo(L_GlobalZeroCoord[0], L_GlobalZeroCoord[1], 1)
        time.sleep(1)
        L_AllLocsWithdrawn = self.TargetManager.GetAllLocsWithdrawn()
        for loc in L_AllLocsWithdrawn:
            self.TargetManager.WinCapturing.UpdateScreenshot()
            LT_Pos = [int(loc[0] - (CalcTarget.SIZE_IMG_CURRENCY/2)), int(loc[1] - (CalcTarget.SIZE_IMG_CURRENCY/2))]
            RT_Pos = [int(loc[0] + (CalcTarget.SIZE_IMG_CURRENCY/2) + 10), int(loc[1] + (CalcTarget.SIZE_IMG_CURRENCY/2) + 10)]
            self.TargetManager.WinCapturing.CropImg(LT_Pos, RT_Pos)
            
            for Currency in list(self.CurrencyCountData.keys()):
                L_CountCurrency = self.GetCountCurrencyFromCurrencyTradeUI(Currency, 0.98, False)
                if (not L_CountCurrency is None) and (L_CountCurrency != 0):
                    self.ChangeCountCurrency(Data.EMathOperation.INC, Currency, L_CountCurrency)
                    break
    
    def SetFieldSuggestion(self, Side: Data.ESideSuggestion, Value):
        self.OpenCurrencyTradeWindow()
        
        if Side == Data.ESideSuggestion.HAVE:
            LocField = CalcTarget.HAVE_FIELD_RSIDE_LOC
        else:
            LocField = CalcTarget.WANT_FIELD_RSIDE_LOC

        pyautogui.moveTo(LocField[0], LocField[1], 0.5)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.keyDown("backspace")
        time.sleep(2)
        pyautogui.keyUp("backspace")
        time.sleep(0.5)
        SetOfValue = str(Value)
        if SetOfValue[0] == "0":
            pyautogui.press("0")
        else:
            for number in SetOfValue:
                pyautogui.press(number)
                time.sleep(0.5)
        
        pyautogui.moveTo(LocField[0], LocField[1] - 30, 0.5)
        time.sleep(0.5)
        pyautogui.click()
    
    def ChooseCurrencyForSuggestion(self, Side: Data.ESideSuggestion, Currency):
        self.OpenCurrencyTradeWindow()
        if Side == Data.ESideSuggestion.HAVE:
            LocField = CalcTarget.HAVE_FIELD_RSIDE_LOC
        else:
            LocField = CalcTarget.WANT_FIELD_RSIDE_LOC
                
    def run(self):
        while True:
            if self.ActionIsActive == False:
                break
            

                           
          
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
    