import cv2 as cv 
import os
import enum
import Debug
import BotAction as bot

UNDER_IMG_OFFSET = 110

class ELocOrient(enum.Enum):
    
    UNDER = 0
    CENTER = 1
       
class TargetManager:
    LootImgNames = None
    DebugMode = None
    ScreenWindow = None
       
    def __init__(self):      
        self.LootImgNames = os.listdir("Loot")
        for index in range(len(self.LootImgNames)):
            self.LootImgNames[index] = "Loot/" + self.LootImgNames[index]
               

    def FindLocLootObject(self):
        for LootPath in self.LootImgNames:
            LocObject = self.FindLocObject(LootPath)
            if not LocObject is None:
                break
        
        return LocObject


    def FindLocObject(self, DesObject_img_path):
        
        DesObject_img = cv.imread(DesObject_img_path, cv.IMREAD_UNCHANGED)
        DesObject_img = cv.cvtColor(DesObject_img, cv.COLOR_RGBA2RGB)
        
        ResultMatch_img = cv.matchTemplate(self.ScreenWindow, DesObject_img, cv.TM_CCOEFF_NORMED)

        MinValMatch, MaxValMatch, NotMatchLoc, LT_ObjectLoc = cv.minMaxLoc(ResultMatch_img)
        if MaxValMatch >= 0.7:
        
            LT_ObjectLoc = int(LT_ObjectLoc[0]), int(LT_ObjectLoc[1])
            SizeHChar_img = DesObject_img.shape[0]
            SizeWChar_img = DesObject_img.shape[1]
            
            RD_ObjectLoc = (LT_ObjectLoc[0] + SizeWChar_img, LT_ObjectLoc[1] + SizeHChar_img)
            
            return LT_ObjectLoc, RD_ObjectLoc
        return None
        
    def GetTargetLoc(self, LocOrient: ELocOrient, LocObject): 
        LT_ObjectLoc = LocObject[0]
        RD_ObjectLoc = LocObject[1]
        if LocOrient == ELocOrient.UNDER:
            SizeWObject = RD_ObjectLoc[0] - LT_ObjectLoc[0]     
            TargetLoc = (int(RD_ObjectLoc[0] - SizeWObject/2), RD_ObjectLoc[1] + UNDER_IMG_OFFSET)
        
        elif LocOrient == ELocOrient.CENTER:
            SizeWObject = RD_ObjectLoc[0] - LT_ObjectLoc[0]
            SizeHObject = RD_ObjectLoc[1] - LT_ObjectLoc[1]     
            TargetLoc = (int(RD_ObjectLoc[0] - SizeWObject/2), int(RD_ObjectLoc[1] - SizeHObject/2))
    
        if Debug.DEBUG_MODE == Debug.EDebugMode.DEBUG_MODE_ON:
            cv.rectangle(self.ScreenWindow, LT_ObjectLoc, RD_ObjectLoc, color=(0,255,0), thickness=2, lineType=cv.LINE_4)     
            cv.drawMarker(self.ScreenWindow, TargetLoc, color=(255,0,255), markerType=cv.MARKER_CROSS)
            cv.imshow("Screen", self.ScreenWindow)

        return TargetLoc
    
    def CheckTarget(self, ScreenWindow):
        bot_state = None
        TargetLoc = None
        self.ScreenWindow = ScreenWindow
        LocObject = self.FindLocLootObject()
        #if not LocObject is None:
        #    bot_state = bot.EBotState.LOOTING
        #    TargetLoc = self.GetTargetLoc(ELocOrient.CENTER, LocObject)
        
        #else:
        #    LocObject = self.FindLocObject("Character.png")
        #    if not LocObject is None:
        #        bot_state = bot.EBotState.FOLLOWING
        #        TargetLoc = self.GetTargetLoc(ELocOrient.UNDER, LocObject)
        LocObject = self.FindLocObject("Character.png")
        if not LocObject is None:
            bot_state = bot.EBotState.FOLLOWING
            TargetLoc = self.GetTargetLoc(ELocOrient.UNDER, LocObject)
        return bot_state, TargetLoc
            