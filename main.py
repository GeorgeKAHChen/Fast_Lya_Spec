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
import Lya_Spec_with_Jaco
import Ori_Lya_Spec
import Initialization
from libpy import Init

torch.set_num_threads(12)
DEBUG = False

class FLS(nn.Module):
    def __init__(self, f, Jf, sequ_t, sequ_tau, delta_t, delta_tau, len_var, loc_rem, device):
        super(FLS, self).__init__()
        self.loc_rem = loc_rem
        self.len_var = len_var
        self.attractor = ode4.ode4(function = f, time_sequ = sequ_t, time_delta = delta_t, device = device)
        self.sub_attr = ode4.ode4(function = f, time_sequ = sequ_tau, time_delta = delta_tau, device = device)
        self.Jacobian = Jacobian.Jacobian(function = Jf, time_delta = delta_tau, device = device)
        #self.Lya_Spec = Lya_Spec.Lya_Spec(time_delta = delta_tau, len_var = len_var, device = device)
        self.Lya_Spec = Lya_Spec.Lya_Spec(time_delta = delta_t, len_var = len_var, device = device)


    def tsequ_to_vec(self, Block):
        Block = torch.cat(Block)
        Block = torch.reshape(Block, (self.len_var, int(len(Block) / self.len_var + 0.1)))
        return Block


    def forward(self, input_x):
        print("Attractor computing")
        Block = self.attractor(input_x)
        Block = Block[self.loc_rem: -1]
        print(len(Block), Block[0].size())
        
        Block = self.tsequ_to_vec(Block)
        print(len(Block), Block[0].size())
        
        print("Sub-attractor computing")
        Block = self.sub_attr(Block)
        print(len(Block), Block[0].size())

        print("Jacobian computing")
        Block = self.Jacobian(Block)
        print(len(Block), len(Block[0]), Block[0][0].size())
        print(Block[0][8][0])

        print("Lyapunov Spectrum computing")
        Block = self.Lya_Spec(Block)
        print(Block)
        print(len(Block), Block[0].size())
        for kase in range(0, len(Block)):
            Block[kase] = torch.mean(Block[kase])

        print(Block)

        return Block



class Multi_init_FLS(nn.Module):
    def __init__(self, f, Jf, sequ_t, delta_t, len_var, device):
        super(Multi_init_FLS, self).__init__()
        #self.attractor = ode4.ode4(function = f, time_sequ = sequ_t, time_delta = delta_t, device = device)
        #self.Jacobian = Jacobian.Jacobian(function = Jf, time_delta = delta_t, device = device)
        #self.Lya_Spec = Lya_Spec.Lya_Spec(time_delta =  delta_t, len_var = len_var, device = device)
        self.Lya_Spec = Ori_Lya_Spec.Ori_Lya_Spec(time_delta =  delta_t, len_var = len_var, device = device, Jfunc = Jf, func = f, time_sequ = sequ_t)


    def forward(self, input_x):
        #print("Attractor computing")
        #Block = self.attractor(input_x)
        #print(len(Block), Block[0].size())

        #print("Jacobian computing")
        #Block = self.Jacobian(Block)
        #print(len(Block), len(Block[0]), Block[0][0].size())

        print("Jacobian and Lyapunov Spectrum computing")
        Block, val_next = self.Lya_Spec(input_x)

        for kase in range(0, len(Block)):
            Block[kase] = torch.mean(Block[kase])
            
        print(Block)

        return Block, val_next



def main():
    # Initialization the dyn sys and parameter
    sequ_t, sequ_tau, f, Jf, model_name, information, initial_val, loc_rem, delta_t, delta_tau, device, group_atta = Initialization.main()
    
    # =======================================================
    # Solution 1
    # =======================================================
    # Define the nn model
    """
    model = FLS(f, Jf, sequ_t, sequ_tau, delta_t, delta_tau, len(initial_val), loc_rem, device).to(device)
    print(model)
    
    # Calculate the LE
    output = model(initial_val)
    """
    # =======================================================
    

    # =======================================================
    # Solution 2
    # =======================================================
    
    # Generate initial values
    print(f, Jf, delta_t, len(initial_val), device)
    model = Multi_init_FLS(f, Jf, sequ_t, delta_t, len(initial_val), device).to(device)
    print(model)
    for kase in range(0, 10):
        import random
        new_val = []
        for i in range(0, len(initial_val)):
            tensor_vec = []
            for j in range(0, 1):    
                #tensor_vec.append(random.random())
                tensor_vec.append(1.0)
            new_val.append(torch.DoubleTensor(tensor_vec))

        initial_val = torch.stack(new_val)
        
        # Calculate the LE

        output = model(initial_val)
        #output = output.tolist()
        #for i in range(0, len(output)):
        #    output[i] = output[i].tolist()
        



        
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.integrate import odeint
        from mpl_toolkits.mplot3d import Axes3D

        x = []
        y = []
        z = []
        for i in range(0, len(output)):
            #output[i] = output[i].tolist()
            x.append(output[i][0].tolist()[0])
            y.append(output[i][1].tolist()[0])
            z.append(output[i][2].tolist()[0])

        fig = plt.figure()
        ax = fig.gca(projection="3d")
        ax.plot(x, y, z, color = "black")
        plt.draw()
        plt.show()
        plt.savefig(str(Init.GetTime()) + ".png")
        
    # =======================================================

    #print(output)
    
    return 


if __name__ == '__main__':
    main()