#==================================================
#
#       Fast Lyapunov Spectrum
#
#       ode4.py
#
#==================================================

import torch
import torch.nn as nn

class ode4(nn.Module):
    def __init__(self, 
                function, 
                time_sequ,
                time_delta,
                debug = False,
                device = "cuda"):
        super(ode4, self).__init__()
        self.function = function
        self.time_sequ = time_sequ
        self.time_delta = time_delta
        self.debug = debug


    def forward(self, input):
        Vals = [input]
        for kase in range(0, len(self.time_sequ)):
            curr_x = Vals[len(Vals) - 1]
            curr_t = self.time_sequ[kase]
            k1 = self.function(curr_x, curr_t)
            k2 = []
            for i in range(0, len(curr_x)):
                k2.append(curr_x[i] + self.time_delta * 0.5 * k1[i]) 
            k2 = self.function(k2, curr_t + self.time_delta * 0.5)
            k3 = []
            for i in range(0, len(curr_x)):
                k3.append(curr_x[i] + self.time_delta * 0.5 * k2[i]) 
            k3 = self.function(k3, curr_t + self.time_delta * 0.5)
            k4 = []
            for i in range(0, len(curr_x)):
                k4.append(curr_x[i] + self.time_delta * k2[i]) 
            k4 = self.function(k4, curr_t + self.time_delta)
            new_x = []
            for i in range(0, len(curr_x)):
                new_x.append(curr_x[i] + self.time_delta * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * (1/6)) 
            if self.debug:
                continue
            Vals.append(new_x)
        return Vals


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
