# MODEL

You can put your model here, or use the original model to get data

### Structure of files
To build a full model, you need

`delta_t` parameter of delta time series (int/float)

* If the `delta_t` parameter is an `int`, then the system is a <b>map</b> rather than a system. The program will use the map calculator rather than the Runge-Kutta method.

`initial_t` Initial time value of the system (int/float)

`final_t` End time value of the system (int/float)

`initial_val` Initial value of the system(list)

<br/><br/>
`model_name` Model file name (str) 

`information` Introduce of the model (str)

<br/><br/> The function of system, return the `np.array` vector of values.

`def Jf(state)` The function of Jacobian Matrix, return the `np.matrix` of the values.

Also you can add other parameter of the system, but they will have no influence of the model calculation or Lyapunov spectrum calculation.


### Example
```
import numpy as np

#System parameter
rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

# Calculation parameter
# For every files, these parameter are necessary and you cannot change their name
delta_t = 0.01
initial_val = [1.0, 1.0, 1.0]
initial_t = 0
final_t = 1000
model_name = "Lorenz"
information = "Lorenz" + "(rho, sigma, beta) = ("  + str(rho) + ", " + str(sigma) + ", " + str(beta) + ")"


# Calculation Function, for dynamic system
def f(state, t):
    x, y, z = state 
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])


# Calculation Function, for Jacobian matrix
def Jf(state):
    #print(state)
    x, y, z = state
    #return Delta_t * np.matrix([[-sigma, sigma, 0], [(rho - z), -1, -x], [y, x, -beta]]) + np.eye(3)
    return np.matrix([[1 - delta_t * sigma,         delta_t * sigma,        0], 
                      [delta_t * (rho - z),         1 - delta_t ,           -delta_t * x], 
                      [delta_t * y,                 delta_t * x,            1 - delta_t * beta]])


```