import matplotlib
matplotlib.use("Agg")
from generate_3b1b_grid import draw_3b1b_escher_grid
import matplotlib.pyplot as plt

# Hack to force PNG output
old_savefig = plt.savefig
def new_savefig(fname, *args, **kwargs):
    old_savefig(str(fname).replace('.svg', '.png'), *args, **kwargs)
    old_savefig(fname, *args, **kwargs)
plt.savefig = new_savefig

draw_3b1b_escher_grid("3b1b_test", recursions=2)

from generate_3b1b_grid import apply_func_to_line, EscherMap
emap = EscherMap(r1=1.0/16.0, r2=1.0, extra_turns=1.0)
wx, wy = apply_func_to_line(-1.0, -1.0, -1.0, -1.0, emap, num_points=2)
print(f"Mapped (-1, -1) -> ({wx[0]}, {wy[0]})")
