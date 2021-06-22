#include <iostream>

using namespace std;

double* func(double *val_k, double vals[3], double t){
    double rho = 28.0;
    double sigma = 10.0;
    double beta = 8.0/3.0;
    double x = vals[0];
    double y = vals[1];
    double z = vals[2];
    //cout << "cnmb" << endl;
    //cout << vals[0] << "\t" << vals[1] << "\t" << vals[2] << endl;

    val_k[0] = sigma * (y - x);
    val_k[1] = x * (rho - z) - y;
    val_k[2] = x * y - beta * z;
    return val_k;
}


 
int main(int argc, char const *argv[])
{  
    double T_max = 1e5;
    double delta_t = 1e-3;
    double curr_t = 0;
    cout << T_max << "\t" << delta_t << endl;
    double curr_x[3];
    double new_x[3];

    int kase = 0;

    for(int i = 0; i < 3; i ++)
        curr_x[i] = 1.0;

    while (1){
        if (curr_t > T_max)     break;
        double nk1[3];
        double nk2[3];
        double nk3[3];
        double nk4[3];
        
        double *k1 = func(nk1, curr_x, curr_t);

        
        for(int i = 0; i < 3; i ++)
            new_x[i] = curr_x[i] + delta_t * 0.5 * k1[i];

        double *k2 = func(nk2, new_x, curr_t + delta_t * 0.5);
   
        for(int i = 0; i < 3; i ++)
            new_x[i] = curr_x[i] + delta_t * 0.5 * k2[i];

        double *k3 = func(nk3, new_x, curr_t + delta_t * 0.5);
        
        for(int i = 0; i < 3; i ++)
            new_x[i] = curr_x[i] + delta_t * k3[i];
       
        double *k4 = func(nk4, new_x, curr_t + delta_t);
        /*
        cout << "vals" << endl;
        cout << k1[0] << "\t" << k1[1] << "\t" << k1[2] << endl;
        cout << k2[0] << "\t" << k2[1] << "\t" << k2[2] << endl;
        cout << k3[0] << "\t" << k3[1] << "\t" << k3[2] << endl;
        cout << k4[0] << "\t" << k4[1] << "\t" << k4[2] << endl;
        */
        for(int i = 0; i < 3; i ++){
            curr_x[i] = curr_x[i] + delta_t * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) /6;
        }
        curr_t += delta_t;
        kase ++;
        //if (kase % 100000 == 0)
            //cout << curr_x[0] << "\t" << curr_x[1] << "\t" << curr_x[2] << "\r";
            //cout << curr_t << "\r";
    }
    cout << curr_x[0] << "\t" << curr_x[1] << "\t" << curr_x[2] << endl;

    cout << endl;
    
    return 0;
}

