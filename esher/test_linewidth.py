import math
geom_scale = 2.0
ratio = 16.0
level_step = max(1, int(round(math.log(ratio) / math.log(geom_scale))))
recursions = 3

for i in range(-level_step, recursions * level_step):
    scale = (1.0 / geom_scale) ** i
    lw = 1.5 * scale
    print(f"i={i:2d}, scale={scale:7.4f}, lw={lw:7.4f}")
