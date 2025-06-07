import enum

class EDebugMode(enum.Enum):
    
    DEBUG_MODE_OFF = 0
    DEBUG_MODE_ON = 1 
    
global DEBUG_MODE
DEBUG_MODE = EDebugMode.DEBUG_MODE_ON