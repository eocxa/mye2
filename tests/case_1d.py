import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from models.charge import Charge
from physics.coulomb import calculate_coulomb_force

def test_1d():
    print("Testing Case 1D...")
    # Dos cargas positivas separadas 1m: deben repelerse
    q1 = Charge(1e-6, 0, 0)
    q2 = Charge(1e-6, 1, 0)
    
    force_on_2 = calculate_coulomb_force(q1, q2)
    print(f"Force on q2: {force_on_2}")
    
    # Magnitud esperada: K * 1e-6 * 1e-6 / 1^2 = 8.987e9 * 1e-12 = 0.008987 N
    expected_mag = 8.9875517923e-3
    assert np.isclose(np.linalg.norm(force_on_2), expected_mag), f"Expected {expected_mag}, got {np.linalg.norm(force_on_2)}"
    assert force_on_2[0] > 0, "Force should be in +X direction (repulsion)"
    print("Case 1D PASSED\n")

if __name__ == "__main__":
    test_1d()
