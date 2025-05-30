import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading
import enum

class EBotState(enum.Enum):
    
    FOLLOWING = 0
    LOOTING = 1

class ActionFollow:
    
    HandleWnd = None
    ActionIsActive = False
    lock = None
    LocUnderObject = None
    LastLocUnderObject = None
    RightMouseButton_isDown = False
    
    def __init__(self):
        self.lock = threading.Lock()
        self.HandleWnd = WinCap.GetWindowHandle()
    
    def UpdateTargetToFollow(self, Target: tuple[int, int]):
        self.lock.acquire()
        self.LocUnderObject = Target
        self.start()
        self.lock.release()

    def start(self):
        if self.ActionIsActive == False:
            self.ActionIsActive = True
            tBotAction = threading.Thread(target=self.run, daemon=True)
            tBotAction.start()

    def stop(self):
        self.ActionIsActive = False
        #pyautogui.mouseUp(button="Right")
        #self.RightMouseButton_isDown = False       
        
    def run(self):
        while True:
            
            time.sleep(0.1)
            if self.ActionIsActive == False:
                break
            if self.LocUnderObject:
                if self.LocUnderObject != self.LastLocUnderObject:
                    
                    #print("Local coord: ", self.LocUnderObject)
                    
                    
                    EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)

                    pyautogui.moveTo(self.LocUnderObject[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                                     self.LocUnderObject[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)
                    
                    if self.RightMouseButton_isDown == False:                     
                        pyautogui.mouseDown(button="Right")
                        self.RightMouseButton_isDown = True
                    self.lock.acquire()
                    self.LastLocUnderObject = self.LocUnderObject
                    self.lock.release() 
                else:
                    if self.RightMouseButton_isDown == True:
                        pyautogui.mouseUp(button="Right")
                        self.RightMouseButton_isDown = False
                        
class ActionLoot:
    
    HandleWnd = None
    ActionIsActive = False
    lock = None
    TargetLoc = None
    LastTargetLoc = None
    
    def __init__(self):
        self.lock = threading.Lock()
        self.HandleWnd = WinCap.GetWindowHandle()
    
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
        while True:
            time.sleep(2)
            if self.ActionIsActive == False:
                break
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