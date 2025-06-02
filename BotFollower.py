import cv2 as cv
import time
import WindowCapture as WinCap
import CalcTarget
import keyboard
import BotAction
import PriorityAction
import BotManagement

TargetManagerObj = CalcTarget.TargetManager()
PriorityManager = PriorityAction.PriorityManager(TargetManagerObj)  #init bot actions
#BotManagementObj = BotManagement.Management(PriorityManager)
#WinCap.PrintAllWindows()
#CurrentTime = time.time()
time.sleep(5)

 
while True:
    
    command = input()
    if command == "stop":
        PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)    
        print("Bot stopped!")
    elif command == "continue":
        PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.ENABLE)
        print("Bot continued!")
    elif command == ("exit" or "close"):
        PriorityManager.ChangeStateCheckingAllActions(BotAction.EStateCheckAction.DISABLE)
        TargetManagerObj.WinCapturing.stop()
        cv.destroyAllWindows()
        print("Exiting!...")
        break
        