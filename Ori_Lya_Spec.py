#==================================================
#
#       Fast Lyapunov Spectrum
#
#       Ori_Lya_Spec.py
#
#==================================================

import torch
import torch.nn as nn

class Ori_Lya_Spec(nn.Module):
    def __init__(self, 
                time_delta,
                len_var,
                Jfunc,
                func,
                time_sequ,
                debug = False,
                device = "cuda"):
        super(Ori_Lya_Spec, self).__init__()
        self.time_delta = time_delta
        self.len_var = len_var
        self.debug = debug
        self.device = device
        self.func = func
        self.Jfunc = Jfunc
        self.time_sequ = time_sequ
        self.len_jaco = 0
        self.size_tensor = 0
        self.multi_table = []
        self.gs_table = []



    def init_cal_table(self):
        line = []
        for i in range(0, self.len_var):
            line.append([n for n in range(self.len_var)])
            for j in range(0, self.len_var):
                line[i][j] += i * self.len_var
            self.gs_table.append([line[i][0], line[i][len(line[i]) - 1]])
        row = []
        for i in range(0, self.len_var):
            tmp = []
            for j in range(0, self.len_var):
                tmp.append(j * self.len_var + i)
            row.append(tmp)

        for i in range(0, len(line)):
            for j in range(0, len(row)):
                self.multi_table.append([line[i], row[j]])

        return 



    def mat_times(self, x1, x2):
        x_ret = []
        for i in range(0, len(self.multi_table)):
            vec = torch.DoubleTensor([0 for n in range(self.size_tensor)])
            for j in range(0, len(self.multi_table[i][0])):
                vec += x1[self.multi_table[i][0][j]] * x2[self.multi_table[i][1][j]]
            x_ret.append(vec)
        return x_ret



    def gram_schmidt(self, x):
        x_ret = []
        for kase in range(0, self.len_var):
            alpha = x[self.gs_table[kase][0]: self.gs_table[kase][1]+1]
            new_alpha = x[self.gs_table[kase][0]: self.gs_table[kase][1]+1]
            for i in range(0, kase):
                beta = x[self.gs_table[i][0]: self.gs_table[i][1]+1]
                inner_beta = torch.DoubleTensor([0 for n in range(self.size_tensor)])
                inner_ab = torch.DoubleTensor([0 for n in range(self.size_tensor)])
                for j in range(0, self.len_var):
                    inner_beta += beta[j] * beta[j]
                    inner_ab += beta[j] * alpha[j]

                for j in range(0, self.len_var):
                    new_alpha[j] -= (inner_ab/inner_beta) * beta[j]
            for j in range(0, self.len_var):
                x_ret.append(new_alpha[j])
        return x_ret



    def normalization(self, x):
        norm_para = []
        for i in range(0, self.len_var):
            vec = torch.DoubleTensor([0 for n in range(self.size_tensor)])
            for j in range(0, self.len_var):
                #print(x[i * self.len_var + j].tolist())
                vec += torch.abs(x[i * self.len_var + j] * x[i * self.len_var + j])
            vec = torch.sqrt(vec)
            norm_para.append(vec)
            for j in range(0, self.len_var):
                x[i * self.len_var + j] /= vec
        return x, norm_para



    def Jacobian(self, x):
        Vals = []
        output = self.Jfunc(x, self.time_delta)
        final = []
        for i in range(len(output)):
            try:
                len(output[i])
            except:
                final.append(torch.DoubleTensor([output[i] for n in range(len(x[0]))]))
            else:
                final.append(output[i])

        Vals.append(final)
        return Vals



    def ode4(self, curr_x, curr_t):
        k1 = self.func(curr_x, curr_t)
        k2 = []
        for i in range(0, len(curr_x)):
            k2.append(curr_x[i] + self.time_delta * 0.5 * k1[i]) 
        k2 = self.func(k2, curr_t + self.time_delta * 0.5)
        k3 = []
        for i in range(0, len(curr_x)):
            k3.append(curr_x[i] + self.time_delta * 0.5 * k2[i]) 
        k3 = self.func(k3, curr_t + self.time_delta * 0.5)
        k4 = []
        for i in range(0, len(curr_x)):
            k4.append(curr_x[i] + self.time_delta * k2[i]) 
        k4 = self.func(k4, curr_t + self.time_delta)
        new_x = []
        for i in range(0, len(curr_x)):
            new_x.append(curr_x[i] + self.time_delta * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * (1/6)) 
        return new_x




    def forward(self, input):
        self.len_jaco = len(input) * len(input)
        self.size_tensor = len(input[0])
        self.init_cal_table()

        eye = []
        is_one = 0
        for i in range(0, self.len_jaco):
            if i == is_one:
                eye.append(torch.DoubleTensor([1.0 for n in range(self.size_tensor)]))
                is_one += self.len_var + 1
            else:
                eye.append(torch.DoubleTensor([0.0 for n in range(self.size_tensor)]))
        
        Lya_Spec = []
        for i in range(0, self.len_var):
            Lya_Spec.append(torch.DoubleTensor([0.0 for n in range(self.size_tensor)]))
        
        input_x = input
        output_x = []
        for kase in range(0, len(self.time_sequ)):
            if kase % 1000 == 0:
                print(kase, len(self.time_sequ), end = "\r")
            #print(Lya_Spec, end = "\r")
            input_x = self.ode4(input_x, self.time_sequ[kase])
            Jaco = self.Jacobian(input_x)[0]
            eye = self.mat_times(Jaco, eye)
            eye = self.gram_schmidt(eye)
            _, norm = self.normalization(eye)
            for i in range(0, self.len_var):
                Lya_Spec[i] = (Lya_Spec[i] * self.time_sequ[kase] + torch.log(norm[i])) / (self.time_sequ[kase] + self.time_delta)
                
        print(len(self.time_sequ), len(self.time_sequ))
        return Lya_Spec, input_x
        #return output_x



    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
