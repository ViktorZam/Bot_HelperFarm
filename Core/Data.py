import enum
import strenum

class EPriorityAction(enum.Enum):
    
    LOW = 0
    MIDDLE = 1
    HIGHT = 2

class EMathOperation(enum.Enum):
    
    SET = 0
    INC = 1
    DEC = 2 

class ESideSuggestion(strenum.StrEnum):
    
    HAVE = "Speculate/HaveWindow.png"
    WANT = "Speculate/WantWindow.png"

class ESuggestionTab(strenum.StrEnum):
    
    IN_STOCK = "Speculate/InStockSugTab.png"
    CURRENCY = "Speculate/CurrencySugTab.png"
    EXPEDITION = "Speculate/ExpeditionSugTab.png"

class EWindow(strenum.StrEnum):
    
    TRADE_CURRENCY_WINDOW = "Speculate/TradeCurrencyWindow.png"
    CHEST_WINDOW = "Speculate/ChestWindow.png"

WINDOW_ACCURACY_EQUAL_DATA = {
    EWindow.TRADE_CURRENCY_WINDOW : 0.94,
    EWindow.CHEST_WINDOW : 0.97,
}

class ETab(strenum.StrEnum):
    
    EXPEDITION_CHEST_TAB = "Speculate/ExpeditionChestTab.png"

class ECurrencyImgPath(enum.Enum):
    
    DIVINE = 0
    CHAOS = 1
    EXALT = 2
    ARTIFACT_ORDER = 3
    COINS = 4

CURRENCY_IMG_PATH = {
    ECurrencyImgPath.DIVINE : ("Speculate/Currency/DivineInStock.png"),
    ECurrencyImgPath.CHAOS : ("Speculate/Currency/ChaosInStock.png"),
    ECurrencyImgPath.EXALT : ("Speculate/Currency/ExaltInStock.png"),
    ECurrencyImgPath.ARTIFACT_ORDER : ("Speculate/Currency/ArtifactOrderInStock.png", "Speculate/Currency/ArtifactOrderInv.png"),
    ECurrencyImgPath.COINS : ("Speculate/Currency/CoinsInStock.png", "Speculate/Currency/CoinsInv.png")
}