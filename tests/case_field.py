import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from models.charge import Charge
from physics.electric_field import calculate_electric_field_at_point

def test_field():
    print("Testing Case Field...")
    # Carga puntual en el origen
    q = Charge(1e-6, 0, 0)
    charges = [q]
    
    # Punto a 1m en X
    point = (1, 0)
    e_field = calculate_electric_field_at_point(point, charges)
    
    print(f"Electric Field at (1,0): {e_field}")
    
    # E = K * q / r^2 = 8.987e9 * 1e-6 / 1 = 8987.55 N/C
    expected_mag = 8.9875517923e3
    assert np.isclose(np.linalg.norm(e_field), expected_mag), f"Expected {expected_mag}, got {np.linalg.norm(e_field)}"
    assert e_field[0] > 0, "Field should point in +X direction"
    print("Case Field PASSED\n")

if __name__ == "__main__":
    test_field()
