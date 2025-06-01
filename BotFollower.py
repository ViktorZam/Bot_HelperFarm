import cv2 as cv
import time
import WindowCapture as WinCap
import CalcTarget
import keyboard
import BotAction as bot
import PriorityAction

TargetManagerObj = CalcTarget.TargetManager()
PriorityManager = PriorityAction.PriorityManager()  #init bot actions
#WinCap.PrintAllWindows()
#CurrentTime = time.time()
time.sleep(5)

 
while True:
    
    command = input()
    if command == "stop":
        

        ActionFollow.stop()
        cv.destroyAllWindows()
        break
    print("Next circle")
        