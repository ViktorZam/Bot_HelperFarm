import enum

class EDebugMode(enum.Enum):
    
    DEBUG_MODE_OFF = 0
    DEBUG_MODE_ON = 1 
    
global DEBUG_MODE
DEBUG_MODE = EDebugMode.DEBUG_MODE_OFF

######## DEBUG field HAVE/WANT START ######### 
#self.OpenCurrencyTradeWindow()
#time.sleep(1)
#self.TargetManager.WinCapturing.UpdateScreenshot()
#cv.rectangle(self.TargetManager.WinCapturing.ScreenWindow, CalcTarget.HAVE_FIELD_LT_LOC, CalcTarget.HAVE_FIELD_RT_LOC, color=(0,255,0), thickness=2, lineType=cv.LINE_4)
#cv.rectangle(self.TargetManager.WinCapturing.ScreenWindow, CalcTarget.WANT_FIELD_LT_LOC, CalcTarget.WANT_FIELD_RT_LOC, color=(0,255,0), thickness=2, lineType=cv.LINE_4)    
#cv.imwrite("Debug/" + str(time.time()) + ".png", self.TargetManager.WinCapturing.ScreenWindow)
######## DEBUG field HAVE/WANT END ######### 