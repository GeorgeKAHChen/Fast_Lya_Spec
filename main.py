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
import Jacobian
import Lya_Spec
import Initialization

class FLS(nn.Module):
    def __init__(self, f, Jf, sequ_t, sequ_tau, delta_t, delta_tau, len_var, loc_rem, device):
        super(FLS, self).__init__()
        self.loc_rem = loc_rem
        self.attractor = ode4.ode4(function = f, time_sequ = sequ_t, time_delta = delta_t, device = device)
        self.sub_attr = ode4.ode4(function = f, time_sequ = sequ_tau, time_delta = delta_tau, device = device)
        self.Jacobian = Jacobian.Jacobian(function = Jf, time_delta = delta_tau, device = device)
        self.Lya_Spec = Lya_Spec.Lya_Spec(time_delta = delta_tau, len_var = len_var, device = device)



    def forward(self, input_x):
        print("Attractor computing")
        Block = self.attractor(input_x)
        
        Block = Block[self.loc_rem: -1]
        Block = torch.DoubleTensor(Block)
        Block = torch.transpose(Block, 0, 1)
        print(len(Block), Block[0].size())

        print("Sub-attractor computing")
        Block = self.sub_attr(Block)
        print(len(Block), Block[0].size())

        print("Jacobian computing")
        Block = self.Jacobian(Block)
        print(len(Block), len(Block[0]), Block[0][0].size())

        print("Lyapunov Spectrum computing")
        Block = self.Lya_Spec(Block)
        print(Block)
        print(len(Block), Block[0].size())
        for kase in range(0, len(Block)):
            Block[kase] = torch.mean(Block[kase])

        print(Block)

        return Block


def main():
    # Initialization the dyn sys and parameter
    sequ_t, sequ_tau, f, Jf, model_name, information, initial_val, loc_rem, delta_t, delta_tau, device, group_atta = Initialization.main()
    
    # Define the nn model
    model = FLS(f, Jf, sequ_t, sequ_tau, delta_t, delta_tau, len(initial_val), loc_rem, device).to(device)
    print(model)
    
    # Calculate the LE
    output = model(initial_val)
    
    return 


if __name__ == '__main__':
    main()