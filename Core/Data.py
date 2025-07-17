import enum

class EPriorityAction(enum.Enum):
    
    LOW = 0
    MIDDLE = 1
    HIGHT = 2

class EMathOperation(enum.Enum):
    
    SET = 0
    INC = 1
    DEC = 2 

class EUIWindow(enum.Enum):
    
    CURRENCY_TRADE = 0
    IN_STOCK = 1