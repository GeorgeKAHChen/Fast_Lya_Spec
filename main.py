#==================================================
#
#       Fast Lyapunov Spectrum
#
#       main.py
#
#==================================================

import torch.nn as nn
import torch
import random
import numpy as np

from layer import ode4
from layer import Jacobian
from layer import Lya_Spec
from layer import Standard

import Initialization

from libpy import Init

torch.set_num_threads(12)
DEBUG = False
Group_vals = 100

class FLS(nn.Module):
    def __init__(self, f, Jf, sequ_t, sequ_tau, delta_t, delta_tau, len_var, loc_rem, device):
        super(FLS, self).__init__()
        self.loc_rem = loc_rem
        self.len_var = len_var
        self.attractor = ode4.ode4(function = f, time_sequ = sequ_t, time_delta = delta_t, device = device)
        self.sub_attr = ode4.ode4(function = f, time_sequ = sequ_tau, time_delta = delta_tau, device = device)
        self.Jacobian = Jacobian.Jacobian(function = Jf, time_delta = delta_tau, device = device)
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
        self.Lya_Spec = Standard.Standard(time_delta =  delta_t, len_var = len_var, device = device, Jfunc = Jf, func = f, time_sequ = sequ_t)


    def forward(self, input_x):
        print("Lyapunov Spectrum computing")
        Block = self.Lya_Spec(input_x)
        print(Block)
        #for kase in range(0, len(Block)):
        #    Block[kase] = torch.mean(Block[kase])
        #print(Block)

        return Block



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
    String = ""
    new_val = []
    for i in range(0, len(initial_val)):
        tensor_vec = []
        for j in range(0, Group_vals):
            tmp = random.random()+initial_val[i].tolist()[0]
            tensor_vec.append(tmp)
            String += str(tmp)
            String += " "
        new_val.append(torch.DoubleTensor(tensor_vec))
        String += "\n"
    initial_val = torch.stack(new_val)
    output = model(initial_val)

    String += "\n\n\n"
    for i in range(0, len(initial_val)):
        output[i] = output[i].tolist()
   
    for j in range(0, Group_vals):
        for i in range(0, len(initial_val)):     
            String += str(output[i][j])
            String += " "
        String += "\n"
    FileName = "Output"
    File = open(FileName, "w")
    File.write(String)
    File.close()
    """
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
    """
    # =======================================================

    #print(output)
    
    return 


if __name__ == '__main__':
    main()