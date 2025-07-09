import time
import Core.WindowCapture as WinCap
import Core.CalcTarget as CalcTarget
import keyboard
import Core.BotAction as BotAction
import sys

time.sleep(3)
TargetManagerObj = CalcTarget.TargetManager(WinCap.ETypeScreening.MANUAL)
ActionSpeculate = BotAction.ActionSpeculate(TargetManagerObj)

while True:
 
    
    time.sleep(1)

        