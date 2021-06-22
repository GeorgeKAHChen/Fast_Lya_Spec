#=========================================
#
#   Generalized Rossler model 
#
#
#=========================================

class model():
    def __init__(self,dimension = 3,
                      a = 0.30,
                      b = 4,
                      d = 2,
                      epsilon = 0.1):
        self.dimension = dimension
        self.a = a
        self.b = b
        self.d = d
        self.epsilon = epsilon
        self.initial_val = [0.8 for n in range(self.dimension)]
        self.model_name = "GR"
        self.information = "GR" + "(dim, a, b, d, epsilon) = (" + str(dimension) + ", " + str(a) + ", " + str(b)+ ", " + str(d)+ ", " + str(epsilon) + ")"
        self.Jf_linear = []


    def f(self, state, t):  
        vals = []
        vals.append(self.a * state[0] - state[1])
        for i in range(1, self.dimension - 1):
            vals.append(state[i-1] - state[i+1])
        vals.append(self.epsilon + self.b * state[self.dimension - 1]*(state[self.dimension - 2] - self.d))
        return vals

    def init_Jf(self, delta_t):
        self.Jf_linear = [0 for n in range(self.dimension*self.dimension)]
        self.Jf_linear[0] = self.a*delta_t + 1
        self.Jf_linear[1] = -delta_t
        for i in range(1, self.dimension - 1):
            self.Jf_linear[i * self.dimension + i - 1] = delta_t
            self.Jf_linear[i * self.dimension + i    ] = 1
            self.Jf_linear[i * self.dimension + i + 1] = - delta_t

    def Jf(self, state, delta_t):
        from copy import deepcopy
        if len(self.Jf_linear) == 0:
            self.init_Jf(delta_t)
        Jf_return = deepcopy(self.Jf_linear)
        Jf_return[(self.dimension - 1) * self.dimension + self.dimension - 2] = self.b * state[self.dimension - 1] * delta_t
        Jf_return[(self.dimension - 1) * self.dimension + self.dimension - 1] = (self.b * state[self.dimension - 2]-self.d*self.b) * delta_t + 1
        return Jf_return
        
    def call_init(self):
        return self.initial_val

    def call_info(self):
        return self.model_name, self.information