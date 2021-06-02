#==================================================
#
#       Fast Lyapunov Spectrum
#
#       Lya_Spec.py
#
#==================================================

import torch
import torch.nn as nn

class Lya_Spec(nn.Module):
    def __init__(self, 
                time_delta,
                len_var,
                debug = False,
                device = "cuda"):
        super(Lya_Spec, self).__init__()
        self.time_delta = time_delta
        self.len_var = len_var
        self.debug = debug
        self.device = device

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
        row = []
        for i in range(0, self.len_var):
            tmp = []
            for j in range(0, self.len_var):
                tmp.append(j * self.len_var + i)
            row.append(tmp)
        self.gs_table = row
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
        beta = [0 for n in range(self.len_jaco)]
        for kase in range(0, self.len_var):
            for j in range(0, self.len_var):
                beta[self.gs_table[kase][j]] = x[self.gs_table[kase][j]]

            for i in range(0, kase):
                inner_beta = torch.DoubleTensor([0 for n in range(self.size_tensor)])
                inner_ab = torch.DoubleTensor([0 for n in range(self.size_tensor)])
                for j in range(0, self.len_var):
                    inner_beta += beta[self.gs_table[i][j]] * beta[self.gs_table[i][j]]
                    inner_ab += beta[self.gs_table[i][j]] * x[self.gs_table[kase][j]]

                for j in range(0, self.len_var):
                    beta[self.gs_table[kase][j]] -= (inner_ab/inner_beta) * beta[self.gs_table[i][j]]

        return beta


    def normalization(self, x):
        norm_para = []
        for i in range(0, self.len_var):
            vec = torch.DoubleTensor([0 for n in range(self.size_tensor)])
            for j in range(0, self.len_var):
                vec += torch.abs(x[i + j * self.len_var] * x[i + j * self.len_var])
            vec = torch.sqrt(vec)
            norm_para.append(vec)
            for j in range(0, self.len_var):
                x[i + j * self.len_var] /= vec

        return x, norm_para




    def forward(self, input):
        self.len_jaco = len(input[0])
        self.size_tensor = len(input[0][0])
        self.init_cal_table()
        #print(self.multi_table)
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
        
        for kase in range(0, len(input)):
            if kase % 1000 == 0:
                print(kase, len(input), end = "\r")
            eye = self.mat_times(input[kase], eye)
            eye = self.gram_schmidt(eye) 
            eye, norm = self.normalization(eye)
            for i in range(0, self.len_var):
                Lya_Spec[i] = (Lya_Spec[i] * (kase*self.time_delta) + torch.log(norm[i])) / ((kase + 1)*self.time_delta)
        print(len(input), len(input))
        return Lya_Spec



    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
