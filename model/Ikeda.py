#=========================================
#
#   Ikeda's model
#
#
#=========================================

import random
import numpy as np

R = 1
C1 = .4
C2 = .9
C3 = 6

delta_t = 1
initial_t = 0
#final_t = 1000000
#final_t = 1e7
final_t = 1e5
#initial_val = [random.random()*10, random.random()*10]
initial_val = [0.1, 0.1]

model_name = "Ikeda"
information = "Ikeda" + "(R, C1, C2, C3) = ("  + str(R) + ", " + str(C1) + ", " + str(C2) + ", " + str(C3) + ")"



def f(state, t):
    x = state[0]
    y = state[1]
    tau = C1 - C3 / (1 + x*x + y*y)
    #print(tau)
    var_sin = np.sin(tau)
    var_cos = np.cos(tau)
    return np.array([R+C2 * (x * var_cos - y * var_sin), 
                       C2 * (x * var_sin + y * var_cos)])


def Jf(state):
    x = state[0]
    y = state[1]

    xi = 1 / (1 + x*x + y*y)
    alpha = 2 * C3 * xi * xi

    tau = C1 - C3 * xi
    var_sin = np.sin(tau)
    var_cos = np.cos(tau)

    para = C2 * np.matrix([[var_cos, -var_sin], 
                             [var_sin,  var_cos]]) 
    para = para * (np.eye(2) + np.matrix([[-y], [x]]) * np.matrix([2 * C3 * x * xi * xi, 2 * C3 * y * xi * xi]))
    return np.matrix(para)

