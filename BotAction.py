import WindowCapture as WinCap
import pyautogui
import win32gui
import time
import threading


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
        
        self.start()
    
    def UpdateTargetToFollow(self, Target: tuple[int, int]):
        self.lock.acquire()
        self.LocUnderObject = Target
        self.lock.release()

    def start(self):
        self.ActionIsActive = True
        tBotAction = threading.Thread(target=self.run, daemon=True)
        tBotAction.start()

    def stop(self):
        self.ActionIsActive = False       
        
    def run(self):
        while True:
            time.sleep(0.1)
            if self.ActionIsActive == False:
                break
            if self.LocUnderObject:
                if self.LocUnderObject != self.LastLocUnderObject:
                    
                    print("Local coord: ", self.LocUnderObject)
                    
                    
                    EdgesWindow = win32gui.GetWindowRect(self.HandleWnd)

                    #win32gui.SetActiveWindow(self.HandleWnd)
                    #win32gui.SetForegroundWindow(self.HandleWnd)
                   
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