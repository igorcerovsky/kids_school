import numpy as np
import matplotlib.pyplot as plt

def test_unwrap():
    # Simulate a line crossing the negative real axis
    t = np.linspace(0, 1, 100)
    x = -1.0 * np.ones_like(t)
    y = np.linspace(1, -1, 100)
    
    # Calculate angles
    angles = np.arctan2(y, x)
    
    # Unwrap angles
    unwrapped_angles = np.unwrap(angles)
    
    print("Original angles min/max:", np.min(angles), np.max(angles))
    print("Unwrapped angles min/max:", np.min(unwrapped_angles), np.max(unwrapped_angles))

test_unwrap()
