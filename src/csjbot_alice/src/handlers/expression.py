#!/usr/bin/env python3

from handlers.base_handler import BaseHandler

class ExpressionHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.MSG_ID = "SET_ROBOT_EXPRESSION_REQ"
        self.EXP_HAPPY = 5000
        self.EXP_SAD = 5001
        # self.EXP_SURPRISE = 5002
        # self.EXP_SMILE = 5003
        self.EXP_ORDINARY = 5004
        self.EXP_ANGRY = 5005
        self.EXP_LIGHTING = 5006
        self.EXP_DOUBLE_BLINK = 5007

        # EXPRESSION_TEARS = 5001
        # EXPRESSION_HEART = 5000
        # EXPRESSION_BLINK = 5004
        # EXPRESSION_FLAME = 5005
        # EXPRESSION_LIGHTNING = 5006
        # EXPRESSION_DOUBLE_BLINK = 5007


    def _action(self, expression, time):
        once = 0
        
        payload = {
            "msg_id": self.MSG_ID,
            "expression": expression,
            "once": once,
            "time": time
        }
        return super()._action(payload)

    def express(self, expression, time=0):
        exp_code = self.get_exp_code(expression)
        return self._action(exp_code, time)
    
    def get_exp_code(self, expression):
        if expression == 'happy':
            return self.EXP_HAPPY

        if expression == 'sad': 
            return self.EXP_SAD

        if expression == 'surprise':    
            return self.EXP_LIGHTING

        if expression == 'smile':                
            return self.EXP_DOUBLE_BLINK

        if expression == 'angry':                            
            return self.EXP_ANGRY

        return self.EXP_ORDINARY


         # EXPRESSION_TEARS = 5001 - SAD
        # EXPRESSION_HEART = 5000 - HAPPY
        # EXPRESSION_BLINK = 5004 - ORDINARY
        # EXPRESSION_FLAME = 5005 - ANGRY
        # EXPRESSION_LIGHTNING = 5006 - SURPRISE
        # EXPRESSION_DOUBLE_BLINK = 5007 - 
