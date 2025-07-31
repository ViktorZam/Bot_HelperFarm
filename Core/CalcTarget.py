import cv2 as cv 
import os
import enum
from Core import Debug
import time
from Core import WindowCapture as WinCap
import numpy
import win32gui
import pyautogui

UNDER_IMG_OFFSET = 110

######## Alva START ############
XY_OFFSET_LEFT_WITHDRAWN_COLUMN1 = (394, 314) # local pos for 1280x800
X_LEN_BETWEEN_WITHDRAWNS = 587 - XY_OFFSET_LEFT_WITHDRAWN_COLUMN1[0]
Y_LEN_BETWEEN_2ROWS = 401 - XY_OFFSET_LEFT_WITHDRAWN_COLUMN1[1]
X_LEN_BETWEEN_LEFT_WITHDRAWNS = 666 - XY_OFFSET_LEFT_WITHDRAWN_COLUMN1[0]

MAX_COUNT_ROW_LOTS = 5
MAX_COUNT_COLUMN_LOTS = 2
MAX_COUNT_LOTS = MAX_COUNT_ROW_LOTS * MAX_COUNT_COLUMN_LOTS

BUTTON_HAVE_LOC = (820, 177) # local pos for 1024x768
BUTTON_WANT_LOC = (450, BUTTON_HAVE_LOC[1])

HAVE_FIELD_CENTER_LOC = (705, 179) # local pos for 1280x800
HAVE_FIELD_LT_LOC = (HAVE_FIELD_CENTER_LOC[0] - 25, HAVE_FIELD_CENTER_LOC[1] - 11)
HAVE_FIELD_RT_LOC = (HAVE_FIELD_CENTER_LOC[0] + 30, HAVE_FIELD_CENTER_LOC[1] + 11)
WANT_FIELD_CENTER_LOC = (570, HAVE_FIELD_CENTER_LOC[1])
WANT_FIELD_LT_LOC = (WANT_FIELD_CENTER_LOC[0] - 25, WANT_FIELD_CENTER_LOC[1] - 11)
WANT_FIELD_RT_LOC = (WANT_FIELD_CENTER_LOC[0] + 30, WANT_FIELD_CENTER_LOC[1] + 11)

CURRENT_CURRENCY_RATE_CENTER_LOC = (636, 146)
CURRENT_CURRENCY_RATE_LT_LOC = (CURRENT_CURRENCY_RATE_CENTER_LOC[0] - 40, CURRENT_CURRENCY_RATE_CENTER_LOC[1] - 8)
CURRENT_CURRENCY_RATE_RT_LOC = (CURRENT_CURRENCY_RATE_CENTER_LOC[0] + 55, CURRENT_CURRENCY_RATE_CENTER_LOC[1] + 8)

COST_TRADE_CENTER_LOC = (CURRENT_CURRENCY_RATE_CENTER_LOC[0], 214)
COST_TRADE_CENTER_LT_LOC = (COST_TRADE_CENTER_LOC[0] - 50, COST_TRADE_CENTER_LOC[1] - 7)
COST_TRADE_CENTER_RT_LOC = (COST_TRADE_CENTER_LOC[0] + 50, COST_TRADE_CENTER_LOC[1] + 7)
######## Alva END ############

######## Char Inventory START ############
XY_OFFSET_FIRST_CHAR_INV_SLOT = (820, 457) # local pos for 1280x800
MAX_COUNT_ROW_CHAR_INV_SLOTS = 5
MAX_COUNT_COLUMN_CHAR_INV_SLOTS = 12
MAX_COUNT_CHAR_INV_SLOTS = MAX_COUNT_ROW_CHAR_INV_SLOTS * MAX_COUNT_COLUMN_CHAR_INV_SLOTS
SIZE_CHAR_INV_SLOT = (cv.imread("Speculate/EmptyInvSlot.png")).shape[0]

GOLD_CENTER_LOC = (920, 652) # local pos for 1280x800
GOLD_LT_LOC = (GOLD_CENTER_LOC[0] - 120, GOLD_CENTER_LOC[1] - 11)
GOLD_RT_LOC = (GOLD_CENTER_LOC[0], GOLD_CENTER_LOC[1] + 11)
######## Char Inventory END ############

######## Chest START ############
SIZE_IMG_CURRENCY = (cv.imread("Speculate/SizeImgCurrency.png")).shape[0]
######## Chest END ############

class ELocOrient(enum.Enum):
    
    UNDER = 0
    CENTER = 1

class ETypeCoord(enum.Enum):
    
    LOCAL = 0
    GLOBAL = 1
       
class TargetManager:
    LootImgNames = None
    DebugMode = None
    WinCapturing = None
       
    def __init__(self, TypeScreening: WinCap.ETypeScreening = WinCap.ETypeScreening.AUTO): 
        self.WinCapturing = WinCap.WindowCap(TypeScreening)     
        self.LootImgNames = os.listdir("Loot")
        for index in range(len(self.LootImgNames)):
            self.LootImgNames[index] = "Loot/" + self.LootImgNames[index]
               

    def FindLocLootObject(self):
        for LootPath in self.LootImgNames:
            LocObject = self.FindLocObject(LootPath)
            if not LocObject is None:
                break
        
        return LocObject


    def FindLocObject(self, Img, ValueMatching=0.94, Encoder=cv.TM_CCORR_NORMED, NewScreen=True):
        
        if isinstance(Img, str):
            DesObject_img = cv.imread(Img, cv.IMREAD_UNCHANGED)
        elif isinstance(Img, cv.typing.MatLike):
            DesObject_img = Img
        #cv.imwrite("Debug/" + str(time.time()) + ".png", DesObject_img)
        DesObject_img = cv.cvtColor(DesObject_img, cv.COLOR_RGBA2RGB)
        
        if NewScreen == True:
            if (self.WinCapturing.TypeScreening == WinCap.ETypeScreening.MANUAL):
                self.WinCapturing.UpdateScreenshot()
        
        if not self.WinCapturing.ScreenWindow is None:
            ResultMatch_img = cv.matchTemplate(self.WinCapturing.ScreenWindow, DesObject_img, Encoder)# TM_CCOEFF_NORMED, TM_CCORR_NORMED
            #cv.imwrite("Debug/" + str(time.time()) + ".png", ResultMatch_img)
            MinValMatch, MaxValMatch, NotMatchLoc, LT_ObjectLoc = cv.minMaxLoc(ResultMatch_img)
            print(MaxValMatch, "///", Img)
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
                #print(MaxValMatch, "///", DesObject_img_path)
                LT_ObjectLoc = int(LT_ObjectLoc[0]), int(LT_ObjectLoc[1])
                SizeHChar_img = DesObject_img.shape[0]
                SizeWChar_img = DesObject_img.shape[1]
                
                RD_ObjectLoc = (LT_ObjectLoc[0] + SizeWChar_img, LT_ObjectLoc[1] + SizeHChar_img)
                
                return LT_ObjectLoc, RD_ObjectLoc
            else:
                return None
        return None
        
    def GetTargetLoc(self, LocOrient: ELocOrient, LocObject, TypeCoord: ETypeCoord=ETypeCoord.GLOBAL): 
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
        
        if TypeCoord == ETypeCoord.GLOBAL:    
            EdgesWindow = win32gui.GetWindowRect(self.WinCapturing.HandleWnd)
            TargetLoc = (TargetLoc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                        TargetLoc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)    
            
            if (TargetLoc[0] > EdgesWindow[2]) or (TargetLoc[1] > EdgesWindow[3]) or (TargetLoc[0] < EdgesWindow[0]) or (TargetLoc[1] < EdgesWindow[1]):
                return None

        return TargetLoc
    
    def ConvertLocalCoordToGlobal(self, Loc: list):
        EdgesWindow = win32gui.GetWindowRect(self.WinCapturing.HandleWnd)
        Loc = (Loc[0] + EdgesWindow[0] + WinCap.BORDER_PIXELS_SIZE,
                Loc[1] + EdgesWindow[1] + WinCap.TITLEBAR_PIXELS_SIZE)  
        return Loc
    
    def GetAllLocsWithdrawn(self, TypeCoord: ETypeCoord = ETypeCoord.LOCAL):
        L_LeftTopLocWithdrawn = XY_OFFSET_LEFT_WITHDRAWN_COLUMN1
        L_AllLocsWithdrawn = []

        for LotIndex in range(MAX_COUNT_LOTS, 0, -1):
            L_LocWithdrawn1 = [0, 0]
            L_LocWithdrawn2 = [0, 0]
            L_LocWithdrawn1[1] = L_LocWithdrawn2[1] = L_LeftTopLocWithdrawn[1] + Y_LEN_BETWEEN_2ROWS * ((LotIndex-1)//MAX_COUNT_COLUMN_LOTS)
                
            L_LocWithdrawn1[0] = L_LeftTopLocWithdrawn[0] + ((LotIndex + 1) % 2) * X_LEN_BETWEEN_LEFT_WITHDRAWNS
            if (TypeCoord == ETypeCoord.GLOBAL):
                L_LocWithdrawn1 = self.ConvertLocalCoordToGlobal(L_LocWithdrawn1)
                L_LocWithdrawn2[1] = L_LocWithdrawn1[1]
            L_AllLocsWithdrawn.append(L_LocWithdrawn1)
            L_LocWithdrawn2[0] = L_LocWithdrawn1[0] + X_LEN_BETWEEN_WITHDRAWNS
            
            L_AllLocsWithdrawn.append(L_LocWithdrawn2)
            
        ##################### Debug BEGIN
        #time.sleep(1)
        #self.WinCapturing.UpdateScreenshot()
        #screen = pyautogui.screenshot()
        #screen = numpy.array(screen)
        #screen = cv.cvtColor(screen, cv.COLOR_RGB2BGR)
        #for loc in L_AllLocsWithdrawn:    
            #cv.drawMarker(screen, loc, color=(255,0,255), markerType=cv.MARKER_CROSS)
        #cv.imwrite("Debug/" + str(time.time()) + ".png", screen)
        #################### Debug END
        
        return L_AllLocsWithdrawn
 
    def GetAllLocsCharInvSlots(self, TypeCoord: ETypeCoord = ETypeCoord.LOCAL):
        L_LeftTopLocCharInvSlot = list(XY_OFFSET_FIRST_CHAR_INV_SLOT)
        L_AllLocsCharInvSlots = []
        L_LocCharInvSlot = list()
        for ColumnSlot in range(MAX_COUNT_COLUMN_CHAR_INV_SLOTS):
            L_XLocCharInvSlot = L_LeftTopLocCharInvSlot[0] + SIZE_CHAR_INV_SLOT * ColumnSlot
            for RowSlot in range(MAX_COUNT_ROW_CHAR_INV_SLOTS):
                L_YLocCharInvSlot = L_LeftTopLocCharInvSlot[1] + SIZE_CHAR_INV_SLOT * RowSlot  
                L_LocCharInvSlot = [L_XLocCharInvSlot, L_YLocCharInvSlot]
                if (TypeCoord == ETypeCoord.GLOBAL):
                    L_LocCharInvSlot = self.ConvertLocalCoordToGlobal(L_LocCharInvSlot)
                
                L_AllLocsCharInvSlots.append(L_LocCharInvSlot)
    
        ##################### Debug BEGIN
        #self.WinCapturing.UpdateScreenshot()
        #for loc in L_AllLocsCharInvSlots:    
            #cv.drawMarker(self.WinCapturing.ScreenWindow, loc, color=(255,0,255), markerType=cv.MARKER_CROSS)
        #cv.imwrite("Debug/" + str(time.time()) + ".png", self.WinCapturing.ScreenWindow)
        #################### Debug END
        return L_AllLocsCharInvSlots