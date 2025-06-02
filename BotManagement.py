import threading
import WindowCapture as WinCap
import time
import win32gui
import PriorityAction
import BotAction

class Management:
    
    HandleWnd = None
    ManagementIsActive = False
    lock = None
    PriorityManager = None

    def __init__(self, PriorityManager: PriorityAction.PriorityManager):
        self.PriorityManager = PriorityManager
        self.lock = threading.Lock()
        self.HandleWnd = WinCap.WindowCap.HandleWnd
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
                self.PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)
            