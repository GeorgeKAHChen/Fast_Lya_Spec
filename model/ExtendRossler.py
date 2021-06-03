#=========================================
#
#   Extended Rossler model 
#
#
#=========================================

class model():
    def __init__(self, 
                 a = 0.25,
                 b = 3,
                 c = 0.5,
                 d = 0.05):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.initial_val = [-10, -6, 0, 10]
        self.model_name = "Extended Rossler"
        self.information = "(a, b, c, d) = ("  + str(a) + " " + str(b) + " "  + str(c) + " "  + str(d) + ")"

    def f(self, state, t):  
        x, y, z, w = state
        return [-y-z, x+self.a*y+w, self.b+x*z, -self.c*z+self.d*w]

    def Jf(self, state, delta_t):
        x, y, z, w = state
        return [1, -delta_t, -delta_t, 0, delta_t, 1+self.a*delta_t, 0, delta_t, z*delta_t, 0, 1+x*delta_t, 0, 0, 0, -self.c*delta_t, 1+self.d*delta_t]

    def call_init(self):
        return self.initial_val

    def call_info(self):
        return self.model_name, self.information