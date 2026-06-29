from generate_3b1b_grid import EscherMap
import numpy as np

emap = EscherMap(r1=1.0/16.0, r2=1.0, extra_turns=1.0)
z_corner = -1.0 - 1.0j
r = np.hypot(z_corner.real, z_corner.imag)
theta = np.arctan2(z_corner.imag, z_corner.real)
log_z = np.log(r) + 1j * theta
w_corner = np.exp(emap.beta * log_z)

C = z_corner / w_corner
print(f"C = {C}")
print(f"Check: w_corner * C = {w_corner * C}")
