import cv2 as cv
import time
import WindowCapture as WinCap
import CalcTarget
import keyboard
import BotAction as bot

TargetManagerObj = CalcTarget.TargetManager()
ELocOrient = CalcTarget.ELocOrient
#WinCap.PrintAllWindows()
#CurrentTime = time.time()
time.sleep(5)

ActionFollow = bot.ActionFollow()
ActionLoot = bot.ActionLoot()    

 
while True:
    
    ScreenWindow = WinCap.GetScreenshot()
    
    if not ScreenWindow is None:       
        bot_state, TargetLoc = TargetManagerObj.CheckTarget(ScreenWindow)
        if bot_state == bot.EBotState.LOOTING:
            ActionLoot.UpdateTargetLoc(TargetLoc)
        elif bot_state == bot.EBotState.FOLLOWING:
            ActionFollow.UpdateTargetToFollow(TargetLoc)
            
            #print ("Mouse position: ", pyautogui.position())
            #print ("Lock to click: ", LocUnderObject)
        #    print(1 / (time.time() - CurrentTime))
        #    CurrentTime = time.time()
        key = cv.waitKey(1)
        if  key == ord('q') or keyboard.is_pressed("q"):
            ActionFollow.stop()
            cv.destroyAllWindows()
            break
        print("Next circle")
        
    else:
        time.sleep(2)