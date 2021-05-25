#==================================================
#
#       Fast Lyapunov Spectrum
#
#       Jacobian.py
#
#==================================================

import torch
import torch.nn as nn

class Jacobian(nn.Module):
    def __init__(self, 
                function, 
                time_delta,
                debug = False,
                device = "cuda"):
        super(Jacobian, self).__init__()
        self.function = function
        self.time_delta = time_delta
        self.debug = debug


    def forward(self, input):
        Vals = []
        for kase in range(0, len(input)):
            input_x = input[kase]
            output = self.function(input_x, self.time_delta)
            final =[]
            for i in range(len(output)):
                try:
                    len(output[i])
                except:
                    final.append(torch.DoubleTensor([output[i] for n in range(len(input_x[0]))]))
                else:
                    final.append(output[i])

            Vals.append(final)
        return Vals


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
