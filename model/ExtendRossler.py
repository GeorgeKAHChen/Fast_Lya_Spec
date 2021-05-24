#=========================================
#
#   Duffing system
#
#
#=========================================
import random
import numpy as np

delta_t = 0.0001
initial_t = 0
final_t = 10
initial_val = [1.0, 1.0, 1.0, 1.0]
model_name = "Extend-Rossler"
information = "Extend-Rossler" + "() = ()"



def f(state, t):
    x, y, z, w = state
    return -y-z, x+0.25*y+w, 3+x*z, -0.5*z+0.05*w

def Jf(state):
    x, y, z, w = state
    return np.matrix([[1        , -delta_t      , -delta_t      , 0             ],
                      [delta_t  , 1+0.25*delta_t, 0             , delta_t       ],
                      [z*delta_t, 0             , 1+x*delta_t   , 0             ],
                      [0        , 0             , -0.5*delta_t  , 1+0.05*delta_t]])
