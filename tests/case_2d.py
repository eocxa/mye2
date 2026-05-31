import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from models.charge import Charge
from physics.net_force import calculate_net_force

def test_2d():
    print("Testing Case 2D...")
    # Triángulo equilátero o similar para probar superposición
    # q1 at (0,0), q2 at (1,0), q3 at (0.5, 0.866)
    q1 = Charge(1e-6, 0, 0)
    q2 = Charge(1e-6, 1, 0)
    q3 = Charge(1e-6, 0.5, 0.866)
    
    charges = [q1, q2, q3]
    net_f_q3 = calculate_net_force(q3, charges)
    
    print(f"Net Force on q3: {net_f_q3}")
    
    # Por simetría, la fuerza neta sobre q3 debería ser puramente vertical (+Y)
    assert np.isclose(net_f_q3[0], 0, atol=1e-5), f"Fx should be ~0, got {net_f_q3[0]}"
    assert net_f_q3[1] > 0, "Fy should be positive (repulsion upwards)"
    print("Case 2D PASSED\n")

if __name__ == "__main__":
    test_2d()
