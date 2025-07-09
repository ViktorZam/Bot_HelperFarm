import threading
from Core import WindowCapture as WinCap
import time
import win32gui
from Core import PriorityAction
from Core import BotAction
import enum    
        
class Management:
    
    HandleWnd = None
    ManagementIsActive = False
    lock = None
    PriorityManager = None
    BotIsActive = None

    def __init__(self, PriorityManager: PriorityAction.PriorityManager):
        self.PriorityManager = PriorityManager
        self.lock = threading.Lock()
        self.HandleWnd = PriorityManager.TargetManager.WinCapturing.HandleWnd
        self.BotIsActive = True
        self.start()
      
    def start(self):
        if self.ManagementIsActive == False:
            self.ManagementIsActive = True
            tManagement = threading.Thread(target=self.run, daemon=True)
            tManagement.start()
    
    def stop(self):
        self.ManagementIsActive = False

    def run(self):
        while True:
            time.sleep(1)
            if self.ManagementIsActive == False:
                break
            
            if self.HandleWnd != win32gui.GetForegroundWindow():
                if self.BotIsActive == True:
                    self.BotIsActive = False
                    self.PriorityManager.stop()
                    self.PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)
                    
            else:
                if self.BotIsActive == False:                   
                    self.BotIsActive = True
                    self.PriorityManager.start()
                    self.PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.ENABLE)