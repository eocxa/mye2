import numpy as np
from physics.vectors import calculate_distance, calculate_unit_vector
K = 8990000000.0

def calculate_coulomb_force(charge1, charge2):
    pos1 = (charge1.x, charge1.y)
    pos2 = (charge2.x, charge2.y)
    r = calculate_distance(pos1, pos2)
    if r == 0:
        raise ValueError('División entre cero: Las cargas no pueden estar en la misma posición.')
    magnitude = K * abs(charge1.q * charge2.q) / r ** 2
    r_hat = calculate_unit_vector(pos1, pos2)
    force_direction = 1 if charge1.q * charge2.q > 0 else -1
    force_vector = force_direction * magnitude * r_hat
    return force_vector