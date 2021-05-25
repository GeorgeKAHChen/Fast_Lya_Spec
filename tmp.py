import torch
import random

multi_table = []
len_var = 3
size_tensor = 10
def init_cal_table():
    global multi_table
    line = []
    for i in range(0, len_var):
        line.append([n for n in range(len_var)])
        for j in range(0, len_var):
            line[i][j] += i * len_var
    row = []
    for i in range(0, len_var):
        tmp = []
        for j in range(0, len_var):
            tmp.append(j * len_var + i)
        row.append(tmp)

    for i in range(0, len(line)):
        for j in range(0, len(row)):
            multi_table.append([line[i], row[j]])
    return 

init_cal_table()
print(multi_table)


def mat_time(x1, x2):
    x_ret = []
    for i in range(0, len(multi_table)):
        vec = torch.Tensor([0 for n in range(size_tensor)])
        for j in range(0, len(multi_table[i])):
            vec += x1[multi_table[i][0][j]] * x2[multi_table[i][1][j]]
        x_ret.append(vec)
    return x_ret

def x():
    return torch.Tensor([random.random(), random.random(), random.random(), random.random(), random.random(), random.random(),random.random(),random.random(),random.random(),random.random()])
x1 = [x(), x(), x(), x(), x(), x(), x(), x(), x()]
x2 = [x(), x(), x(), x(), x(), x(), x(), x(), x()]
print(x1)
print(x2)
print(mat_time(x1, x2))

def normalization(x):
    norm_para = []
    for i in range(0, len_var):
        vec = torch.DoubleTensor([0 for n in range(size_tensor)])
        for j in range(0, len_var):
            vec += x[i * len_var + j] * x[i * len_var + j]
        vec = torch.sqrt(vec)
        norm_para.append(torch.sqrt(vec))
        for j in range(0, len_var):
            x[i * len_var + j] /= vec

    return x, norm_para
print(normalization(mat_time(x1, x2)))