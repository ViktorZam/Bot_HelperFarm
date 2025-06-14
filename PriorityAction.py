import threading
import time
import BotAction
import CalcTarget
import DataPriority


class PriorityManager:
    
    CheckingHightPriorityAction = False
    lock = None
    BotLowActions = {}
    BotMiddleActions = {}
    BotHightActions = {}
    BotPriorityActions = [BotHightActions, BotMiddleActions, BotLowActions]
    TargetManager = None

    def __init__(self, TargetManager: CalcTarget.TargetManager):
        self.TargetManager = TargetManager
        self.lock = threading.Lock()
        #L_BotActions = {"Follow" : BotAction.ActionFollow(self.TargetManager),
                        #"Loot" : BotAction.ActionLoot(self.TargetManager)}
        L_BotActions = {"Loot" : BotAction.ActionLoot(self.TargetManager)}
        for index in range(len(L_BotActions)):
            
            L_ActionNames = list(L_BotActions.keys())
            L_Actions = list(L_BotActions.values())
            self.AddBotAction(L_ActionNames[index], L_Actions[index])
            
        self.start()
        
        
    def AddBotAction(self, NameAction, BotAction: BotAction.ActionBase):
        
        if BotAction.Priority == DataPriority.EPriorityAction.LOW:
            self.BotLowActions.update({NameAction : BotAction})
        elif BotAction.Priority == DataPriority.EPriorityAction.MIDDLE:
            self.BotMiddleActions.update({NameAction : BotAction})
        elif BotAction.Priority == DataPriority.EPriorityAction.HIGHT:
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
                if Action.ActionIsActive == True:
                    if NextAction != Action:
                        Action.stop()
                    else:
                        #print("Next action is active - ", Action)
                        pass

                else:
                    if NextAction == Action:
                        Action.start()
                        #print("Next action - ", Action)
                        
                           
    def ChangeStateCheckingAllActions(self, StateAction: BotAction.EStateCheckAction):
        for TypeActions in self.BotPriorityActions:    
            for Action in TypeActions.values():
                if StateAction == BotAction.EStateCheckAction.ENABLE:
                    Action.start_check_ReadyAction()
                elif StateAction == BotAction.EStateCheckAction.DISABLE:
                    Action.stop()
                    Action.stop_check_ReadyAction()                     

    def run(self):
        while True:
            
            time.sleep(1)
            if self.CheckingHightPriorityAction == False:
                break
            
            L_ExitFromCheck = False
            for TypeActions in self.BotPriorityActions:
 
                for Action in TypeActions.values():
                                
                    if Action.ActionIsActive == True:
                        L_ExitFromCheck = True
                        #print("action is active: ", Action.Priority, " - ", Action)   
                        break
                    if Action.ActionIsReady == True:
                        self.ActivateAction(Action) 
                        L_ExitFromCheck = True
                        #print("action is ready: ", Action.Priority, " - ", Action)    
                        break
                    
                if L_ExitFromCheck == True:
                    break
            #print("------------------------")