import threading
import time
from Core import BotAction
from Core import CalcTarget
from Core import DataPriority
import sys
import strenum

class EBotActions(strenum.StrEnum):
    
    FOLLOW = "FOLLOW"
    LOOT = "LOOT" 


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
        L_BotActions = {}
        L_argv = sys.argv
        L_argv.pop(0)
        
        for arg in L_argv:
            if (arg == EBotActions.FOLLOW):
                L_BotActions.update(FOLLOW = BotAction.ActionFollow(self.TargetManager))
            elif (arg == EBotActions.LOOT):
                L_BotActions.update(LOOT = BotAction.ActionLoot(self.TargetManager))

        #L_BotActions = {"Follow" : BotAction.ActionFollow(self.TargetManager),
                        #"Loot" : BotAction.ActionLoot(self.TargetManager)}
        #L_BotActions = {"Loot" : BotAction.ActionLoot(self.TargetManager)}
        #L_BotActions = {"Follow" : BotAction.ActionFollow(self.TargetManager)}
        
        for index in range(len(L_BotActions)):
            
            L_ActionNames = list(L_BotActions.keys())
            L_Actions = list(L_BotActions.values())
            self.AddBotAction(L_ActionNames[index], L_Actions[index])
            
        self.start()
        
        
    def AddBotAction(self, NameAction, BotAction: BotAction.ActionCheckReady):
        
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
    
    def ActivateAction(self, NextAction: BotAction.ActionCheckReady):
        #print(NextAction)
        for TypeActions in self.BotPriorityActions:    
            for Action in TypeActions.values():           
                if Action.ActionIsActive == True:
                    if NextAction != Action:
                        Action.stop()
                        #print("action is stoped - ", Action)
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
            if self.CheckingHightPriorityAction == False:
                break
            
            L_ExitFromCheck = False
            for TypeActions in self.BotPriorityActions:
                
                for Action in TypeActions.values():
                    #print(Action)            
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
            time.sleep(0.5)
            #print("------------------------")