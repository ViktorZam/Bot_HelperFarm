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
    EXPEDITION_DEAL_WINDOW = "Speculate/ExpeditionDealWindow.png"
    ROG_WINDOW = "Speculate/RogWindow.png"
    CHAR_INV_WINDOW = "Speculate/CharInventory.png"

ACCORDANCE_WINDOW_AND_CHAR = {
    EWindow.ROG_WINDOW : "Speculate/Rog.png",
    
}


WINDOW_ACCURACY_EQUAL_DATA = {
    EWindow.TRADE_CURRENCY_WINDOW : 0.94,
    EWindow.CHEST_WINDOW : 0.97,
}

class ETab(strenum.StrEnum):
    
    EXPEDITION_CHEST_TAB = "Speculate/ExpeditionChestTab.png"

class ECurrencyName(strenum.StrEnum):
    
    DIVINE = "DIVINE"
    CHAOS = "CHAOS"
    EXALT = "EXALT"
    ARTIFACT_ORDER = "ARTIFACT_ORDER"
    COINS = "COINS"

CURRENCY_IMG_PATH = {
    ECurrencyName.DIVINE : ("Speculate/Currency/DivineInStock.png", "Speculate/Currency/ArtifactOrderInv.png"),
    ECurrencyName.CHAOS : ("Speculate/Currency/ChaosInStock.png", "Speculate/Currency/ArtifactOrderInv.png"),
    ECurrencyName.EXALT : ("Speculate/Currency/ExaltInStock.png", "Speculate/Currency/ArtifactOrderInv.png"),
    ECurrencyName.ARTIFACT_ORDER : ("Speculate/Currency/ArtifactOrderInStock.png", "Speculate/Currency/ArtifactOrderInv.png"),
    ECurrencyName.COINS : ("Speculate/Currency/CoinsInStock.png", "Speculate/Currency/CoinsInv.png")
}

class ETypePickCurrency(enum.Enum):
    
    ONE_STACK = 0
    ALL = 1
