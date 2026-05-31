import numpy as np
from physics.vectors import calculate_distance, calculate_unit_vector

# Constante de Coulomb en N·m²/C²
K = 8.9875517923e9

def calculate_coulomb_force(charge1, charge2):
    """
    Calcula el vector de fuerza que ejerce charge1 sobre charge2.
    F = K * |q1 * q2| / r^2
    """
    pos1 = (charge1.x, charge1.y)
    pos2 = (charge2.x, charge2.y)
    
    r = calculate_distance(pos1, pos2)
    
    if r == 0:
        raise ValueError("División entre cero: Las cargas no pueden estar en la misma posición.")
        
    # Magnitud de la fuerza
    magnitude = K * abs(charge1.q * charge2.q) / (r**2)
    
    # Dirección: si son del mismo signo se repelen, si son distintos se atraen
    # El vector unitario r_hat apunta de 1 a 2.
    # Si q1*q2 > 0 (repulsión), la fuerza sobre 2 tiene la dirección de r_hat.
    # Si q1*q2 < 0 (atracción), la fuerza sobre 2 tiene la dirección opuesta a r_hat.
    r_hat = calculate_unit_vector(pos1, pos2)
    
    force_direction = 1 if (charge1.q * charge2.q) > 0 else -1
    
    force_vector = force_direction * magnitude * r_hat
    
    return force_vector
