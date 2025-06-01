import enum
import threading
import BotAction
import time

class EPriorityAction(enum.Enum):
    
    LOW = 0
    MIDDLE = 1
    HIGHT = 2

class PriorityManager:
    
    CheckingHightPriorityAction = False
    lock = None
    BotLowActions = dict[str, BotAction.ActionBase]
    BotMiddleActions = dict[str, BotAction.ActionBase]
    BotHightActions = dict[str, BotAction.ActionBase]
    BotPriorityActions = [BotHightActions, BotMiddleActions, BotLowActions]
    
    def __init__(self):
        self.lock = threading.Lock()
        L_BotActions = {"Follow" : BotAction.ActionFollow(),
                        "Loot" : BotAction.ActionLoot()}
        for index in range(len(L_BotActions)):
            
            L_ActionNames = L_BotActions.keys()
            L_Actions = L_BotActions.values()
            self.AddBotAction(L_ActionNames[index], L_Actions[index])
            
        self.start()
        
        
    def AddBotAction(self, NameAction, BotAction: BotAction.ActionBase):
        
        if BotAction.Priority == EPriorityAction.LOW:
            self.BotLowActions.update({NameAction : BotAction})
        elif BotAction.Priority == EPriorityAction.MIDDLE:
            self.BotMiddleActions.update({NameAction : BotAction})
        elif BotAction.Priority == EPriorityAction.HIGHT:
            self.BotHightActions.update({NameAction : BotAction})
        

    def start(self):
        if self.CheckingHightPriorityAction == False:
            self.CheckingHightPriorityAction = True
            tCheckingHightPriorityAction = threading.Thread(target=self.run, daemon=True)
            tCheckingHightPriorityAction.start()
    
    def stop(self):
        self.CheckingHightPriorityAction = False
    
    def ActivateAction(self, NextAction: BotAction.ActionBase):
        for TypeActions in self.BotPriorityActions:    
            for Action in TypeActions.values():
                Action = BotAction.ActionBase(Action)            
                if Action.ActionIsActive == True:
                    if NextAction == Action:
                        Action.start()
                    else:
                        Action.stop()
                           
    def ChangeStateAllActions(Self, StateAction: BotAction.EStateAction):
        if StateAction == BotAction.EStateAction.ENABLE:
            pass                      
                        
        

    def run(self):
        while True:
            
            time.sleep(1)
            if self.CheckingHightPriorityAction == False:
                break
            
            
            ExitFromCheck = False
            for TypeActions in self.BotPriorityActions:
                
                for Action in TypeActions.values():
                    Action = BotAction.ActionBase(Action)            
                    if Action.ActionIsActive == True:
                        ExitFromCheck = True   
                        break
                    if Action.ActionIsReady == True:
                        self.ActivateAction(Action) 
                        ExitFromCheck = True
                        break
                    
                if ExitFromCheck == True:
                    break