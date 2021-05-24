#=========================================
#
#   Generalized Rossler(GR) System
#
#
#=========================================
import random
import numpy as np
from copy import deepcopy

dimension = 7
a = 0.32
b = 4
d = 2
epsilon = 0.1
delta_t = 0.0001
initial_t = 0
final_t = 10
model_name = "GR"
information = "GR" + "(dim, a, b, d, epsilon) = (" + str(dimension) + ", " + str(a) + ", " + str(b)+ ", " + str(d)+ ", " + str(epsilon) + ")"

initial_val = []
for i in range(0, dimension):
    initial_val.append(random.random())

Jf_linear = [[0 for n in range(dimension)] for n in range(dimension)]
Jf_linear[0][0] = a*delta_t + 1
Jf_linear[0][1] = -delta_t
for i in range(1, dimension - 1):
    Jf_linear[i][i-1] = delta_t
    Jf_linear[i][i] = 1
    Jf_linear[i][i+1] = - delta_t



def f(state, t):
    vals = []
    vals.append(a * state[0] - state[1])
    for i in range(1, dimension - 1):
        vals.append(state[i-1] - state[i+1])
    vals.append(epsilon + b * state[dimension - 1]*(state[dimension - 2] - d))
    return vals



def Jf(state):
    Jf_return = deepcopy(Jf_linear)
    Jf_return[dimension - 1][dimension - 2] = b * state[dimension - 1] * delta_t
    Jf_return[dimension - 1][dimension - 1] = (b * state[dimension - 2]-d*b) * delta_t + 1
    return np.matrix(Jf_return)
