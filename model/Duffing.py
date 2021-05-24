#=========================================
#
#   Duffing system
#
#
#=========================================
import random
import numpy as np
val_alpha = 1
val_beta = 0.04
val_gamma = 1
val_delta = 0.1
val_omega = np.pi / 2

delta_t = 0.0001
initial_t = 0
final_t = 10
initial_val = [1.0, 1.0]
model_name = "Duffing"
information = "Duffing" + "(alpha, beta, gamma, delta, omega) = ("  + str(val_alpha) + ", " + str(val_beta) + ", " + str(val_gamma) + ", " + str(val_delta) + ", " + str(val_omega) + ")"


def f(state, t):
    x, y = state
    return y, val_gamma * np.cos(val_omega * t) - val_alpha * x - val_beta * x * x *x - val_delta * y

def Jf(state):
    x, y = state
    return np.matrix([[1,                                               -delta_t                ], 
                      [(-val_alpha - 3 * val_beta * x * x) * delta_t,   val_delta * delta_t + 1 ]])
