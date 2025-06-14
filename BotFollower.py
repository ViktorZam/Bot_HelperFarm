import cv2 as cv
import time
import WindowCapture as WinCap
import CalcTarget
import keyboard
import BotAction
import PriorityAction
import BotManagement

time.sleep(5)
TargetManagerObj = CalcTarget.TargetManager()
PriorityManager = PriorityAction.PriorityManager(TargetManagerObj)  #init bot actions
BotManagementObj = BotManagement.Management(PriorityManager)
#WinCap.PrintAllWindows()
#CurrentTime = time.time()


 
while True:
    
    command = input()
    if command == "stop":
        PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)    
        print("Bot stopped!")
    elif command == "continue":
        PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.ENABLE)
        print("Bot continued!")
    elif command == ("exit" or "close"):
        if BotManagementObj.BotIsActive == True:
            PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)
        TargetManagerObj.WinCapturing.stop()
        cv.destroyAllWindows()
        print("Exiting!...")
        break
        