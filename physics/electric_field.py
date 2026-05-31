import numpy as np
from physics.vectors import calculate_distance, calculate_unit_vector

# Constante de Coulomb en N·m²/C²
K = 8.9875517923e9

def calculate_electric_field_at_point(point_pos, charges):
    """
    Calcula el vector de campo eléctrico en un punto (x, y) debido a un conjunto de cargas.
    E = K * q / r^2 * r_hat
    donde r_hat apunta de la carga al punto.
    """
    e_field = np.array([0.0, 0.0])
    
    for charge in charges:
        charge_pos = (charge.x, charge.y)
        r = calculate_distance(charge_pos, point_pos)
        
        if r == 0:
            # Según los requerimientos, debemos impedir el cálculo sobre una carga
            continue 
            
        r_hat = calculate_unit_vector(charge_pos, point_pos)
        
        # E = K * q / r^2
        magnitude = K * charge.q / (r**2)
        
        e_field += magnitude * r_hat
        
    return e_field
