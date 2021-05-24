#=========================================
#
#   Henon's model
#
#
#=========================================

import random
import numpy as np

a = 1.4
#b = -0.3
b = 0.3

delta_t = 1
initial_t = 0
final_t = 1e5
#initial_val = [random.random()/10, random.random()/10]
initial_val = [0.1, 0.1]

model_name = "Henon"
information = "Henon" + "(a, b) = ("  + str(a) + ", " + str(b) + ")"



def f(state, t):
    x = state[0]
    y = state[1]
    return np.array([a -  x * x + b * y, x])


def Jf(state):
    x = state[0]
    y = state[1]
    return np.matrix([[-2*x, b], [1, 0]])


