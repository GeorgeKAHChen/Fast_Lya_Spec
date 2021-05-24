#==================================================
#
#       Fast Lyapunov Spectrum
#
#       main.py
#
#==================================================

import torch.nn as nn
import torch

import ode4
from libpy import Init
import Initialization
sequ_t, sequ_tau, f, Jf, model_name, information, initial_val, loc_rem, delta_t, delta_tau, device = Initialization.main()
class FLS(nn.Module):
    def __init__(self):
        super(FLS, self).__init__()
        self.attractor = ode4.ode4(function = f, time_sequ = sequ_t, time_delta = delta_t, debug = False)
        self.sub_attr = ode4.ode4(function = f, time_sequ = sequ_tau, time_delta = delta_tau, debug = True)
        """
        self.Jacobian = jaco.jaco(func = Jf)
        self.Lya_Spec = Lya_Spec.Lya_Spec()
        """
    def forward(self, input_x):
        print("Attractor computing")
        Block = self.attractor(input_x)
        Block = Block[loc_rem: -1]
        Block = torch.DoubleTensor(Block)
        print(Block)
        Block = torch.transpose(Block, 0, 1)
        print(Block[0]) 
        print("sub-attractor computing")
        Block = self.sub_attr(Block)
        return Block
        #Block = Block[loc_rem: len(Block)]
        #Block = self.sub_attr(Block)
        #Block = self.Jacobian(Block)
        #Local_LE = self.Lya_Spec(Block)
        #Global_LE = torch.mean(Local_LE)
        #return Global_LE

def main():
    model = FLS().to(device)
    print(model)
    output = model(initial_val)
    #print(output)


if __name__ == '__main__':
    main()