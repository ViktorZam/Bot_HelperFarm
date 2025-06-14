import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum
import DataPriority
import CalcTarget

class EStateCheckAction(enum.Enum):
    
    DISABLE = 0
    ENABLE = 1


class ActionBase:
    
    HandleWnd = None
    ActionIsActive = False
    CheckingReadyAction = False
    ActionIsReady = False
    lock = None
    TargetLoc = None
    LastTargetLoc = None
    Priority = None
    TargetManager = None
    
    def __init__(self, TargetManager:  CalcTarget.TargetManager):
        self.TargetManager = TargetManager
        self.lock = threading.Lock()
        self.HandleWnd = self.TargetManager.WinCapturing.HandleWnd
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


class ActionFollow(ActionBase):

    RightMouseButton_isDown = False
    Priority = DataPriority.EPriorityAction.MIDDLE

    def run_check_ReadyAction(self):
         while True:
            
            time.sleep(1)
            if self.CheckingReadyAction == False:
                break
            
            LocObject = self.TargetManager.FindLocObject("Character.png")
            if not LocObject is None:
                self.ActionIsReady = True
            else:
                self.ActionIsReady = False
                self.stop()

    def stop(self):
        super().stop()
        pyautogui.mouseUp(button="Right")
        self.RightMouseButton_isDown = False       
        
    def run(self):
        while True:
            if self.ActionIsActive == False:
                break
            time.sleep(0.1) #0.1

            LocObject = self.TargetManager.FindLocObject("Character.png")
                
            if not LocObject is None:
                self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.UNDER, LocObject)
                if self.TargetLoc:
                    if self.TargetLoc != self.LastTargetLoc:

                        EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)

                        pyautogui.moveTo(self.TargetLoc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                                            self.TargetLoc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)
                            
                        if self.RightMouseButton_isDown == False:                     
                            pyautogui.mouseDown(button="Right")
                            self.RightMouseButton_isDown = True
                        self.lock.acquire()
                        self.LastTargetLoc = self.TargetLoc
                        self.lock.release() 
                    else:
                        if self.RightMouseButton_isDown == True:
                            pyautogui.mouseUp(button="Right")
                            self.RightMouseButton_isDown = False
                        
class ActionLoot(ActionBase):      
    
    Priority = DataPriority.EPriorityAction.HIGHT  
    
    def run_check_ReadyAction(self):
         while True:
            
            time.sleep(1)
            if self.CheckingReadyAction == False:
                break
            LocObject = self.TargetManager.FindLocLootObject()
            #print(LocObject)
            if not LocObject is None:
                self.ActionIsReady = True
            else:
                self.ActionIsReady = False
                self.stop()
 
    def run(self):
        while True:
            time.sleep(2)
            if self.ActionIsActive == False:
                break
            
            LocObject = self.TargetManager.FindLocLootObject()
            #print (LocObject)
            if not LocObject is None:
                self.TargetLoc = self.TargetManager.GetTargetLoc(CalcTarget.ELocOrient.CENTER, LocObject)
            if self.TargetLoc:
                if self.TargetLoc != self.LastTargetLoc:
                    print("Local coord Loot: ", self.TargetLoc) 
                    EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)  
                    pyautogui.moveTo(self.TargetLoc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                                    self.TargetLoc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)
                    pyautogui.click()
                    self.lock.acquire()
                    self.LastTargetLoc = self.TargetLoc
                    self.lock.release() 
