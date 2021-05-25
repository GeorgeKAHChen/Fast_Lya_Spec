#==================================================
#
#       Fast Lyapunov Spectrum
#
#       Initialization.py
#
#==================================================

def main():
    #==================================================
    # Import json
    from libpy.Init import read_json
    import os
    json_file = read_json(os.path.join(os.getcwd(), "config.json"))
    t_max = json_file["t_max"]
    t_rem = json_file["t_rem"]
    delta_t = json_file["delta_t"]
    tau_max = json_file["tau_max"]
    delta_tau = json_file["delta_tau"]
    device = json_file["device"]
    group_atta = json_file["group_atta"]
    #==================================================

    #==================================================
    # Import model
    dyn = json_file["dyn"]
    dyn = __import__(dyn, fromlist=["model"])
    dyn = getattr(dyn, "model")()
    #==================================================

    #==================================================
    # Check Parameter
    import sys
    if t_rem >= t_max:
        print("JSON ERROR: t_rem < t_max is necessary.")
        sys.exit(0)
    if device == "cuda" or device == "cpu":
        pass
    else:
        print("JSON ERROR: 'device' should be 'cuda' for gpu learning or 'cpu' for cpu learning.")
        sys.exit(0)
    #==================================================

    #==================================================
    # Check model
    from torch import DoubleTensor 
    initial_val = []
    try:
        dyn_init = dyn.call_init()
        for i in range(0, len(dyn_init)):
            initial_val.append(DoubleTensor([dyn_init[i]]))
    except:
        print("MODEL ERROR: Model files should include a 'initial_val' as the initial value of the system.")
        sys.exit(0)
    try:
        dyn.f(initial_val, 0)
    except:
        print("MODEL ERROR: Model files should include a 'f' function to computing the system.")
        sys.exit(0)
    try:
        dyn.Jf(initial_val, delta_t)
    except:
        print("MODEL ERROR: Model files should include a 'Jf' function to computing the Jacobian matrix of the system.")
        sys.exit(0)
    try:
        print(dyn.call_info)
    except:
        print("MODEL ERROR: model should include a model_name and a information string")
        sys.exit(0)
    #==================================================

    #==================================================
    # Initial time sequence
    sequ_t = [0]
    sequ_tau = [0]
    loc_rem = 0
    while 1:
        if sequ_t[len(sequ_t)-1] + delta_t >= t_max:
            break
        if loc_rem == 0:
            if sequ_t[len(sequ_t)-1] + delta_t > t_rem:
                loc_rem = len(sequ_t)
        sequ_t.append(sequ_t[len(sequ_t)-1] + delta_t)
    while 1:
        if sequ_tau[len(sequ_tau)-1] + delta_tau >= tau_max:
            break
        sequ_tau.append(sequ_tau[len(sequ_tau)-1] + delta_tau)
    #==================================================

    return sequ_t, sequ_tau, dyn.f, dyn.Jf, dyn.model_name, dyn.information, initial_val, loc_rem, delta_t, delta_tau, device, group_atta


if __name__ == '__main__':
    main()