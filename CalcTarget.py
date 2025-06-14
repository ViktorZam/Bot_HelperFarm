import cv2 as cv 
import os
import enum
import Debug
import time
import WindowCapture as WinCap

UNDER_IMG_OFFSET = 110

class ELocOrient(enum.Enum):
    
    UNDER = 0
    CENTER = 1
       
class TargetManager:
    LootImgNames = None
    DebugMode = None
    WinCapturing = None
       
    def __init__(self): 
        self.WinCapturing = WinCap.WindowCap()     
        self.LootImgNames = os.listdir("Loot")
        for index in range(len(self.LootImgNames)):
            self.LootImgNames[index] = "Loot/" + self.LootImgNames[index]
               

    def FindLocLootObject(self):
        for LootPath in self.LootImgNames:
            LocObject = self.FindLocObject(LootPath, 0.9)
            if not LocObject is None:
                break
        
        return LocObject


    def FindLocObject(self, DesObject_img_path, ValueMatching):
        
        DesObject_img = cv.imread(DesObject_img_path, cv.IMREAD_UNCHANGED)
        #cv.imwrite("123.png", DesObject_img)
        DesObject_img = cv.cvtColor(DesObject_img, cv.COLOR_RGBA2RGB)
        if not self.WinCapturing.ScreenWindow is None:
            ResultMatch_img = cv.matchTemplate(self.WinCapturing.ScreenWindow, DesObject_img, cv.TM_CCOEFF_NORMED)# TM_CCOEFF_NORMED, TM_CCORR_NORMED
            #cv.imwrite(str(time.time()) + ".png", self.WinCapturing.ScreenWindow)
            #cv.imshow("Screen", ResultMatch_img)
            #cv.waitKey(1000)
            MinValMatch, MaxValMatch, NotMatchLoc, LT_ObjectLoc = cv.minMaxLoc(ResultMatch_img)
            print(MaxValMatch, "///", DesObject_img_path)
            if MaxValMatch >= ValueMatching:#0.7
            
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
            self.WinCapturing.SetDebugLocs(LT_ObjectLoc, RD_ObjectLoc, TargetLoc)
          
        return TargetLoc
            