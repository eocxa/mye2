import numpy as np
from physics.coulomb import calculate_coulomb_force

def calculate_net_force(target_charge, other_charges):
    net_force = np.array([0.0, 0.0])
    for charge in other_charges:
        if charge is target_charge:
            continue
        force = calculate_coulomb_force(charge, target_charge)
        net_force += force
    return net_force