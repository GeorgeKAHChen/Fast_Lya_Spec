#=========================================
#
#   Lorenz model 
#
#
#=========================================

class model():
    def __init__(self, rho = 28.0, sigma = 10.0, beta = 8.0/3.0):
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.initial_val = [1.0, 1.0, 1.0]
        self.model_name = "Lorenz"
        self.information = "(rho, sigma, beta) = ("  + str(rho) + ", " + str(sigma) + ", " + str(beta) + ")"

    def f(self, state, t):  
        x, y, z = state 
        return [self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z]

    def Jf(self, state, delta_t):
        x, y, z = state
        return [1-delta_t*self.sigma, delta_t*self.sigma, 0, delta_t*(self.rho - z), 1-delta_t, -delta_t*x, delta_t*y, delta_t*x, 1-delta_t*self.beta]

    def call_init(self):
        return self.initial_val

    def call_info(self):
        return self.model_name, self.information