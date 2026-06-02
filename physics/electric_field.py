import numpy as np
from physics.vectors import calculate_distance, calculate_unit_vector
K = 8990000000.0

def calculate_electric_field_at_point(point_pos, charges):
    e_field = np.array([0.0, 0.0])
    for charge in charges:
        charge_pos = (charge.x, charge.y)
        r = calculate_distance(charge_pos, point_pos)
        if r == 0:
            raise ValueError(f'No se puede calcular el campo eléctrico exactamente en la posición de la carga (r=0).')
        r_hat = calculate_unit_vector(charge_pos, point_pos)
        magnitude = K * charge.q / r ** 2
        e_field += magnitude * r_hat
    return e_field