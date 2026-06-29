import numpy as np
from generate_3b1b_grid import apply_func_to_line, EscherMap
emap = EscherMap(r1=1.0/16.0, r2=1.0, extra_turns=1.0)
cell_size = 0.25
segments = [
    (-1.0, -1.0, -1.0 + cell_size, -1.0),
    (-1.0 + cell_size, -1.0, -1.0 + cell_size, -1.0 + cell_size),
    (-1.0 + cell_size, -1.0 + cell_size, -1.0, -1.0 + cell_size),
    (-1.0, -1.0 + cell_size, -1.0, -1.0)
]
for i, (px0, py0, px1, py1) in enumerate(segments):
    wx, wy = apply_func_to_line(px0, py0, px1, py1, emap, num_points=50)
    print(f"Seg {i}: start ({wx[0]:.2f}, {wy[0]:.2f}) end ({wx[-1]:.2f}, {wy[-1]:.2f})")
