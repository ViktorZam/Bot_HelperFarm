import cv2 as cv 

def FindLocObject(DesObject_img_path, MainScreen_img):
    
    DesObject_img = cv.imread(DesObject_img_path, cv.IMREAD_UNCHANGED)
    DesObject_img = cv.cvtColor(DesObject_img, cv.COLOR_RGBA2RGB)
    
    ResultMatch_img = cv.matchTemplate(MainScreen_img, DesObject_img, cv.TM_CCOEFF_NORMED)

    MinValMatch, MaxValMatch, NotMatchLoc, LT_ObjectLoc = cv.minMaxLoc(ResultMatch_img)
    LT_ObjectLoc = int(LT_ObjectLoc[0]), int(LT_ObjectLoc[1])
    SizeHChar_img = DesObject_img.shape[0]
    SizeWChar_img = DesObject_img.shape[1]

    RD_ObjectLoc = (LT_ObjectLoc[0] + SizeWChar_img, LT_ObjectLoc[1] + SizeHChar_img)
    
    return LT_ObjectLoc, RD_ObjectLoc
    
    
def GetLockUnderObject(LT_ObjectLoc, RD_ObjectLoc): 
    
    SizeWObject = RD_ObjectLoc[0] - LT_ObjectLoc[0]     
    LocUnderObject = (int(RD_ObjectLoc[0] - SizeWObject/2), RD_ObjectLoc[1] + 20)
    
    return LocUnderObject