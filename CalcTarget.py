import cv2 as cv 
import os
import enum
import Debug
import time
import WindowCapture as WinCap
import numpy
import win32gui

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
            LocObject = self.FindLocObject(LootPath, cv.TM_CCORR_NORMED)
            if not LocObject is None:
                break
        
        return LocObject


    def FindLocObject(self, DesObject_img_path, ValueMatching=0.94, Encoder=cv.TM_CCORR_NORMED):
        
        DesObject_img = cv.imread(DesObject_img_path, cv.IMREAD_UNCHANGED)
        #cv.imwrite(str(time.time()) + ".png", DesObject_img)
        DesObject_img = cv.cvtColor(DesObject_img, cv.COLOR_RGBA2RGB)
        if not self.WinCapturing.ScreenWindow is None:
            ResultMatch_img = cv.matchTemplate(self.WinCapturing.ScreenWindow, DesObject_img, Encoder)# TM_CCOEFF_NORMED, TM_CCORR_NORMED
            #cv.imwrite("Debug/" + str(time.time()) + ".png", ResultMatch_img)
            MinValMatch, MaxValMatch, NotMatchLoc, LT_ObjectLoc = cv.minMaxLoc(ResultMatch_img)
            #print(MaxValMatch, "///", DesObject_img_path)
            ##################### Debug BEGIN
            #LT_ObjectLoc = int(LT_ObjectLoc[0]), int(LT_ObjectLoc[1])
            #SizeHChar_img = DesObject_img.shape[0]
            #SizeWChar_img = DesObject_img.shape[1]   
            #RD_ObjectLoc = (LT_ObjectLoc[0] + SizeWChar_img, LT_ObjectLoc[1] + SizeHChar_img)
            #cv.rectangle(ResultMatch_img, LT_ObjectLoc, RD_ObjectLoc, color=(0,255,0), thickness=2, lineType=cv.LINE_4)
            #ResultMatch_img = (ResultMatch_img * 255).astype(numpy.uint8) #for TM_CCORR_NORMED
            #cv.imwrite("Debug/" + str(time.time()) + ".png", ResultMatch_img)
            #cv.imshow("Screen", ResultMatch_img)
            #cv.waitKey(1000)
            #################### Debug END
            if MaxValMatch >= ValueMatching:#0.9
            
                LT_ObjectLoc = int(LT_ObjectLoc[0]), int(LT_ObjectLoc[1])
                SizeHChar_img = DesObject_img.shape[0]
                SizeWChar_img = DesObject_img.shape[1]
                
                RD_ObjectLoc = (LT_ObjectLoc[0] + SizeWChar_img, LT_ObjectLoc[1] + SizeHChar_img)
                
                return LT_ObjectLoc, RD_ObjectLoc
            else:
                return None
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
            
        EdgesWindow = win32gui.GetWindowRect(self.WinCapturing.HandleWnd)
        TargetLoc = (TargetLoc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                     TargetLoc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)    
            
        if (TargetLoc[0] > EdgesWindow[2]) or (TargetLoc[1] > EdgesWindow[3]):
            return None

        return TargetLoc
            