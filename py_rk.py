
def func(vals, t):
    rho = 28.0
    sigma = 10.0
    beta = 8.0/3.0
    x = vals[0]
    y = vals[1]
    z = vals[2]

    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z



 
def main():
    T_max = 1000
    delta_t = 1e-3
    curr_x = [1.0, 1.0, 1.0]
    curr_t = 0
    kase = 0
    new_x = [0, 0, 0]

    while curr_t < T_max:
        k1 = func(curr_x, curr_t);

        for i in range(0, 3):
            new_x[i] = curr_x[i] + delta_t * 0.5 * k1[i];

        k2 = func(new_x, curr_t + delta_t * 0.5);
   
        for i in range(0, 3):
            new_x[i] = curr_x[i] + delta_t * 0.5 * k2[i];

        k3 = func(new_x, curr_t + delta_t * 0.5);
        
        for i in range(0, 3):
            new_x[i] = curr_x[i] + delta_t * k3[i];
       
        k4 = func(new_x, curr_t + delta_t);

        for i in range(0, 3):
            curr_x[i] = curr_x[i] + delta_t * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) /6;
        
        curr_t += delta_t
        kase += 1
        #if kase % 1000 == 0:
        #    print(curr_x[0], curr_x[1], curr_x[2], end = "\r")

    return 0;

main()