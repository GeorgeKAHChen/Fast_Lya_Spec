#=========================================
#
#   Rossler system
#
#
#=========================================
import random
import numpy as np
a = 0.2
b = 0.2
c = 5.7


delta_t = 0.0001
initial_t = 0
final_t = 10
initial_val = [1.0, 1.0, 1.0]
model_name = "Rossler"
information = "Rossler" + "(a, b, c) = ("  + str(a) + ", " + str(b) + ", " + str(c) + ")"


def f(state, t):
    x, y, z = state
    return - y - z, x + a * y, b + z * (x - c)


def Jf(state):
    x, y, z = state
    #return Delta_t * np.matrix([[-sigma, sigma, 0], [(rho - z), -1, -x], [y, x, -beta]]) + np.eye(3)
    return np.matrix([[1,               -delta_t,                   -delta_t], 
                      [delta_t,         a * delta_t + 1 ,           0], 
                      [delta_t * z,     0,                          (x - c) * delta_t + 1]])
