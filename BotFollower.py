import cv2 as cv
import time
import WindowCapture as WinCap
import CalcTarget
import enum
import keyboard
import BotAction

class EDebugMode(enum.Enum):
    
    DEBUG_MODE_OFF = 0
    DEBUG_MODE_ON = 1  
    
  
DebugMode = EDebugMode.DEBUG_MODE_ON
#WinCap.PrintAllWindows()
#CurrentTime = time.time()

ActionFollow = BotAction.ActionFollow()    

 
while True:

    ScreenWindow = WinCap.GetScreenshot()
    
    if not ScreenWindow is None:

        LT_LocObject, RD_LocObject = CalcTarget.FindLocObject("Fire.png", ScreenWindow)
        LocUnderObject = CalcTarget.GetLockUnderObject(LT_LocObject, RD_LocObject)
        
        if DebugMode == EDebugMode.DEBUG_MODE_ON:
            cv.rectangle(ScreenWindow, LT_LocObject, RD_LocObject, color=(0,255,0), thickness=2, lineType=cv.LINE_4)     
            cv.drawMarker(ScreenWindow, LocUnderObject, color=(255,0,255), markerType=cv.MARKER_CROSS)
            cv.imshow("Screen", ScreenWindow) 
        
        ActionFollow.UpdateTargetToFollow(LocUnderObject)
        
        #print ("Mouse position: ", pyautogui.position())
        #print ("Lock to click: ", LocUnderObject)
    #    print(1 / (time.time() - CurrentTime))
    #    CurrentTime = time.time()
        key = cv.waitKey(2000)
        if  key == ord('q') or keyboard.is_pressed("q"):
            ActionFollow.stop()
            cv.destroyAllWindows()
            break
        print("all done")
        
    else:
        time.sleep(2)