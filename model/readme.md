# MODEL

You can add your own model here. 

You can change the <a href="https://github.com/GeorgeKAHChen/Fast_Lya_Spec/blob/master/model/SAMPLE.py">SAMPLE.py</a> directly with following introduction.

#### About the model file

A model files always include 5 class at least with the class name `model`, the `__init__`, `f`, `Jf`, `call_init`, `call_info`. Typically you just need to change the `__init__`, `f` as well as `Jf` to construct your model. However, I will still show you every function and their usage.

##### `__init__`
The `__init__` is the typical initial function in python, in this function, you need include 

`self.initial_val` (arr[val]) as the initial value of the system.

`self.model_name` (str) as the name of the model

`self.information` (str) as the introduce of the model

Otherwise, you can define the parameter of the system here. The following example include a parameter called `para`

```Python
def __init__(self, para = 1):
    self.para = para
    self.initial_val = [1.0]
    self.model_name = "SAMPLE"
    self.information = "para = ("  + str(para) + ")"
```

For example, in Lorenz system 
```Python
def __init__(self, rho = 28.0, sigma = 10.0, beta = 8.0/3.0):
    self.rho = rho
    self.sigma = sigma
    self.beta = beta
    self.initial_val = [1.0, 1.0, 1.0]
    self.model_name = "Lorenz"
    self.information = "(rho, sigma, beta) = ("  + str(rho) + ", " + str(sigma) + ", " + str(beta) + ")"
```

##### `f`
The `f` function is the differential equation you want to calculate. The input of the function always be `state` as the input x value and `t` as the time value. 

```Python
def f(self, state, t):  
    x = state 
    return f(x)
```

For example, the Lorenz system

```Python
def f(self, state, t):  
    x, y, z = state 
    return self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z
```

where the `self.sigma`, `self.beta` and `self.rho` be parameter which you defined in `__init__`

##### `Jf`
`Jf` means Jacobian function of the system. However that is not the Jacobian of the system, here you need to calculate the numerical iteration formular based on the Jacobian by yourself. For instance, if a system have system Jacobian matrix J(x), then the iteration Jacobian is I + delta_t * J(x)

The input of the system include a value `state` and `delta_t`.

Sample 
```Python
def Jf(self, state, delta_t):
    x = state
    return J_{delta_t}(x)
```

Sample in Lorenz
```Python
def Jf(self, state, delta_t):
    x, y, z = state
    return 1-delta_t*self.sigma, delta_t*self.sigma, 0, delta_t*(self.rho - z), 1-delta_t, -delta_t*x, delta_t*y, delta_t*x, 1-delta_t*self.beta
```

##### `call_init`
This function will return the initial value directly. Typically you don't need to change it.


##### `call_info`
This function will return the name  as well as the information(for instance, you can print the parameter of the model in this information) of the model directly. Typically you don't need to change it.

