#=========================================
#
#   SAMPLE model 
#
#
#=========================================

class model():
    def __init__(self, para = 1):
        self.para = para
        self.initial_val = [1.0]
        self.model_name = "SAMPLE"
        self.information = "para = ("  + str(para) + ")"

    def f(self, state, t):  
        x = state 
        return f(x)

    def Jf(self, state, delta_t):
        x = state
        return J_{delta_t}(x)
        
    def call_init(self):
        return self.initial_val

    def call_info(self):
        return self.model_name, self.information