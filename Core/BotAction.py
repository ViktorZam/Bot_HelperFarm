from Core import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum
from Core import DataPriority
from Core import CalcTarget
import cv2 as cv

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
    Priority = DataPriority.EPriorityAction.MIDDLE

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
    
    Priority = DataPriority.EPriorityAction.HIGHT  
    
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
    
    Gold = 0
    
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        super().__init__(TargetManager)
        LocObject = self.TargetManager.FindLocObject("Speculate/CharInventory.png", 0.95)
        if LocObject is None:
            pyautogui.press("i")
            
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1) 
        
        LocObject = self.TargetManager.FindLocObject("Speculate/TradeComplete.png", 0.52)
        if not LocObject is None:
            self.OpenCurrencyTradeWindow()
            self.PickingCurrencyFromAlvaTradeWindow()

        LocObject = self.TargetManager.FindLocObject("Speculate/TradeCurrencyWindow.png")
        if not LocObject is None:
            pyautogui.press("esc")
            time.sleep(1)        
              
        if (self.IsEmptyCharInv() == False):
            self.OpenChest()
            self.TargetManager.GetAllLocsCharInvSlots(CalcTarget.ETypeCoord.LOCAL)

            
            
            
            
        
               
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
        pass
    
    def IsEmptyCharInv(self):
        self.TargetManager.WinCapturing.UpdateScreenshot()
        
        L_ImgShape = self.TargetManager.WinCapturing.ScreenWindow.shape
        heightScreen = int(L_ImgShape[0])
        widthScreen = int(L_ImgShape[1])
        L_ImgShape = cv.imread("Speculate/EmptyInvSlot.png")
        L_ImgShape = L_ImgShape.shape
        SizeSlotImg = int(L_ImgShape[0])
        for value in range(1, 5):
            if value == 1:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = int(CalcTarget.XY_OFFSET_FIRST_CHAR_INV_SLOT[0] - ((SizeSlotImg/2) + 5))
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 2:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = int(CalcTarget.XY_OFFSET_FIRST_CHAR_INV_SLOT[1] - ((SizeSlotImg/2) + 5))
                
            elif value == 3:
                X_LT_CoordRectangle = 0
                Y_LT_CoordRectangle = int(CalcTarget.XY_OFFSET_FIRST_CHAR_INV_SLOT[1] + ((SizeSlotImg/2) + 5))
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = heightScreen
                
            elif value == 4:
                X_LT_CoordRectangle = int(CalcTarget.XY_OFFSET_FIRST_CHAR_INV_SLOT[0] + ((SizeSlotImg/2) + 5))
                Y_LT_CoordRectangle = 0
                X_RD_CoordRectangle = widthScreen
                Y_RD_CoordRectangle = heightScreen
                
            cv.rectangle(self.TargetManager.WinCapturing.ScreenWindow, (X_LT_CoordRectangle, Y_LT_CoordRectangle), 
                        (X_RD_CoordRectangle, Y_RD_CoordRectangle), color=(255,255,255), thickness=-1) 
            
        #cv.imwrite("Debug/" + str(time.time()) + ".png", self.TargetManager.WinCapturing.ScreenWindow)    
        LocObject = self.TargetManager.FindLocObject("Speculate/EmptyInvSlot.png", NewScreen=False)
        if not LocObject is None:
            return True
        else:
            return False

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
    