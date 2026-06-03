import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from models.charge import Charge
from physics.coulomb import calculate_coulomb_force

def test_1d():
    print('Testing Case 1D...')
    q1 = Charge(1e-06, 0, 0)
    q2 = Charge(1e-06, 1, 0)
    force_on_2 = calculate_coulomb_force(q1, q2)
    print(f'Force on q2: {force_on_2}')
    expected_mag = 0.00899
    assert np.isclose(np.linalg.norm(force_on_2), expected_mag), f'Expected {expected_mag}, got {np.linalg.norm(force_on_2)}'
    assert force_on_2[0] > 0, 'Force should be in +X direction (repulsion)'
    print('Case 1D PASSED\n')
if __name__ == '__main__':
    test_1d()