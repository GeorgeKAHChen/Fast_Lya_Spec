#=========================================
#
#   Rossler model 
#
#
#=========================================

class model():
    def __init__(self, a = 0.2, b = 0.2, c = 5.7):
        self.a = a
        self.b = b
        self.c = c
        self.initial_val = [1.0, 1.0, 1.0]
        self.model_name = "Rossler"
        self.information = "(a, b, c) = ("  + str(a) + ", " + str(b) + ", " + str(c) + ")"

    def f(self, state, t):  
        x, y, z = state 
        return [- y - z, x + self.a * y, self.b + z * (x - self.c)]

    def Jf(self, state, delta_t):
        x, y, z = state
        return [1, -delta_t, -delta_t, delta_t, self.a * delta_t + 1, 0, delta_t * z, 0, (x - self.c) * delta_t + 1]

    def call_init(self):
        return self.initial_val

    def call_info(self):
        return self.model_name, self.information

