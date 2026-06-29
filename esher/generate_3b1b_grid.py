import argparse
import cmath
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

OUTPUT_DIR = Path(__file__).parent / "output_escher"

class EscherMap:
    def __init__(self, r1: float, r2: float, extra_turns: float = 0.0):
        self.r1 = r1
        self.r2 = r2
        self.extra_turns = extra_turns
        self.log_ratio = math.log(r2 / r1)
        # Lenstra's exact formula for Escher's Print Gallery:
        # alpha = (2*pi*i) / (ln(256) + 2*pi*i)
        # where ln(256) is log_ratio
        numerator = complex(0, extra_turns * 2 * math.pi)
        denominator = complex(self.log_ratio, extra_turns * 2 * math.pi)
        if abs(denominator) == 0:
            self.beta = complex(1.0, 0.0)
        else:
            self.beta = numerator / denominator
            
        # Compute rotation factor C so that (-1, -1) maps to (-1, -1)
        z_corner = -1.0 - 1.0j
        r = math.hypot(z_corner.real, z_corner.imag)
        theta = math.atan2(z_corner.imag, z_corner.real)
        log_z = complex(math.log(r), theta)
        w_corner = cmath.exp(self.beta * log_z)
        self.C = z_corner / w_corner

def bilinear_sample(img_arr: np.ndarray, px: np.ndarray, py: np.ndarray) -> np.ndarray:
    H, W, C = img_arr.shape
    px = np.clip(px, 0, W - 1 - 1e-9)
    py = np.clip(py, 0, H - 1 - 1e-9)

    x0 = np.floor(px).astype(np.int32)
    x1 = x0 + 1
    y0 = np.floor(py).astype(np.int32)
    y1 = y0 + 1

    wa = (x1 - px) * (y1 - py)
    wb = (px - x0) * (y1 - py)
    wc = (x1 - px) * (py - y0)
    wd = (px - x0) * (py - y0)

    wa = wa[..., np.newaxis]
    wb = wb[..., np.newaxis]
    wc = wc[..., np.newaxis]
    wd = wd[..., np.newaxis]

    sampled = (wa * img_arr[y0, x0] +
               wb * img_arr[y0, x1] +
               wc * img_arr[y1, x0] +
               wd * img_arr[y1, x1])
    return sampled

def warp_image_conformal(img_array: np.ndarray, emap: EscherMap, width: int = 1200, height: int = 1200) -> np.ndarray:
    x = np.linspace(-1.0, 1.0, width)
    y = np.linspace(1.0, -1.0, height)
    xx, yy = np.meshgrid(x, y)
    w = xx + 1j * yy
    w_unrotated = w / emap.C
    w_unrotated = np.where(w_unrotated == 0, 1e-12 + 1e-12j, w_unrotated)
    
    # We want z such that w_unrotated = z^beta
    # ln(w_unrotated) = beta * ln(z) -> ln(z) = ln(w_unrotated) / beta
    z_unscaled = np.exp(np.log(w_unrotated) / emap.beta)
    
    N = np.maximum(np.abs(np.real(z_unscaled)), np.abs(np.imag(z_unscaled)))
    N_safe = np.maximum(N, 1e-12)

    ratio = emap.r2 / emap.r1

    k = np.floor(-np.log(N_safe) / emap.log_ratio)
    z_scaled = z_unscaled * (ratio ** k)

    src_h, src_w, src_c = img_array.shape
    px = (np.real(z_scaled) + 1.0) * 0.5 * (src_w - 1)
    py = (1.0 - np.imag(z_scaled)) * 0.5 * (src_h - 1)

    warped_img = bilinear_sample(img_array, px, py)
    
    origin_mask = (np.abs(w) < 1e-10)
    warped_img[origin_mask] = 255.0

    return warped_img.astype(np.uint8)

def create_nested_image(img_array: np.ndarray, emap: EscherMap, width: int = 1200, height: int = 1200) -> np.ndarray:
    x = np.linspace(-1.0, 1.0, width)
    y = np.linspace(1.0, -1.0, height)
    xx, yy = np.meshgrid(x, y)

    N = np.maximum(np.abs(xx), np.abs(yy))
    N_safe = np.maximum(N, 1e-12)

    ratio = emap.r2 / emap.r1

    k = np.floor(-np.log(N_safe) / emap.log_ratio)
    xx_scaled = xx * (ratio ** k)
    yy_scaled = yy * (ratio ** k)

    src_h, src_w, _ = img_array.shape
    px = (xx_scaled + 1.0) * 0.5 * (src_w - 1)
    py = (1.0 - yy_scaled) * 0.5 * (src_h - 1)

    nested_img = bilinear_sample(img_array, px, py)
    return nested_img.astype(np.uint8)

def complex_pow(z: complex, beta: complex) -> complex:
    if abs(z) < 1e-12:
        return 0j
    r = abs(z)
    theta = math.atan2(z.imag, z.real)
    log_z = complex(math.log(r), theta)
    return cmath.exp(beta * log_z)

def apply_func_to_line(x0, y0, x1, y1, emap, num_points=200):
    """Maps a line segment in the complex plane through the Escher transform."""
    t = np.linspace(0, 1, num_points)
    x = x0 + t * (x1 - x0)
    y = y0 + t * (y1 - y0)
    
    # Use numpy to compute radius and angle
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    
    # Unwrap the angle to prevent branch cut jumps!
    # This fixes the "overlapping" criss-crossing lines in Matplotlib.
    theta = np.unwrap(theta)
    
    # Calculate log(z) and then the conformal mapping w = exp(beta * log(z)) * C
    log_z = np.log(r) + 1j * theta
    w = np.exp(emap.beta * log_z) * emap.C
    
    return w.real, w.imag

def get_nested_square_grid_lines(grid_size, height, scale_factor):
    """
    Generates a Cartesian grid of lines with a hole in the middle.
    This exactly mimics Manim's Square().get_grid(grid_size, grid_size)
    with the central squares removed.
    """
    lines = []
    H = height
    h = height / scale_factor
    
    for i in range(grid_size + 1):
        pos = -H + (2 * H * i) / grid_size
        
        # Avoid floating point exact comparisons by adding a tiny epsilon
        eps = 1e-9
        
        # Vertical line at x = pos
        if -h + eps < pos < h - eps:
            # Line crosses the interior of the hole, split it
            lines.append((pos, H, pos, h))
            lines.append((pos, -h, pos, -H))
        else:
            lines.append((pos, H, pos, -H))
            
        # Horizontal line at y = pos
        if -h + eps < pos < h - eps:
            # Line crosses the interior of the hole, split it
            lines.append((H, pos, h, pos))
            lines.append((-h, pos, -H, pos))
        else:
            lines.append((H, pos, -H, pos))
            
    return lines

def draw_3b1b_escher_grid(filename, ratio=16.0, extra_turns=1.0, grid_size=16, recursions=2, image_path=None):
    """
    Generates the pure mathematically transformed grid following the 3b1b logic.
    Plots both the straight unwarped grid and the final Escher warped grid.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12), facecolor="#FDFCF7")
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("Original Droste Grid", fontsize=24, pad=20)
    
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title("Escher Print Gallery Grid", fontsize=24, pad=20)
    
    emap = EscherMap(r1=1.0/ratio, r2=1.0, extra_turns=extra_turns)
    
    import matplotlib.patches as patches
    
    # Mark the lower left square on the original grid and its mapped version
    cell_size = 0.25 
    
    # Draw original lower left square
    lower_left_rect = patches.Rectangle((-1.0, -1.0), cell_size, cell_size, 
                                        linewidth=0, facecolor="#F2C94C", alpha=0.7, zorder=1)
    ax1.add_patch(lower_left_rect)
    
    # Draw warped lower left square
    w_poly_x, w_poly_y = [], []
    for px0, py0, px1, py1 in [
        (-1.0, -1.0, -1.0 + cell_size, -1.0),
        (-1.0 + cell_size, -1.0, -1.0 + cell_size, -1.0 + cell_size),
        (-1.0 + cell_size, -1.0 + cell_size, -1.0, -1.0 + cell_size),
        (-1.0, -1.0 + cell_size, -1.0, -1.0)
    ]:
        wx, wy = apply_func_to_line(px0, py0, px1, py1, emap, num_points=50)
        w_poly_x.extend(wx)
        w_poly_y.extend(wy)
    ax2.fill(w_poly_x, w_poly_y, color="#F2C94C", alpha=0.7, zorder=1)
    
    if image_path:
        with Image.open(image_path) as img:
            img_rgb = img.convert("RGB")
            img_array = np.array(img_rgb)
        
        nested_img = create_nested_image(img_array, emap, 1200, 1200)
        warped_img = warp_image_conformal(img_array, emap, 1200, 1200)
        
        ax1.imshow(nested_img, extent=[-1.0, 1.0, -1.0, 1.0], zorder=0)
        ax2.imshow(warped_img, extent=[-1.0, 1.0, -1.0, 1.0], zorder=0)
    
    # Base Cartesian grid covering [-1.0, 1.0] but with hole at [-0.5, 0.5]
    geom_scale = 2.0
    base_lines = get_nested_square_grid_lines(grid_size=8, height=1.0, scale_factor=geom_scale)
    
    base_linewidth = 1.5
    decay_factor = 0.85
    
    # Apply recursive scaling and non-linear line width decay
    level_step = max(1, int(round(math.log(ratio) / math.log(geom_scale))))
    H_val = 1.0 
    
    for i in range(-4, recursions * 4):
        scale = (1.0 / geom_scale) ** i
        is_base_scale = (i == 0 or i == level_step)
        
        lw = max(0.1, base_linewidth * (decay_factor ** i)) if i >= 0 else base_linewidth
        
        # We only draw if the line is thick enough to be visible
        if lw < 0.05:
            continue
            
        for (x0, y0, x1, y1) in base_lines:
            # Scale coordinates down for this recursion level
            sx0, sy0 = x0 * scale, y0 * scale
            sx1, sy1 = x1 * scale, y1 * scale
            
            # Identify if this is a perimeter line of the fundamental domain square
            # A vertical line has x0 == x1, and is on perimeter if abs(x0) == H_val
            # A horizontal line has y0 == y1, and is on perimeter if abs(y0) == H_val
            is_perimeter = ((abs(x0 - x1) < 1e-9 and abs(abs(x0) - H_val) < 1e-9) or 
                            (abs(y0 - y1) < 1e-9 and abs(abs(y0) - H_val) < 1e-9))
            
            is_thick = is_base_scale and is_perimeter
            cur_lw_ax1 = lw * 3.0 if is_thick else lw
            z_ax1 = 4 if is_thick else 2
            color_ax1 = "#27AE60" if is_thick else "#1F5DB9"
            alpha_ax1 = 1.0 if is_thick else 0.9
            
            # Map through the Escher transform
            wx, wy = apply_func_to_line(sx0, sy0, sx1, sy1, emap)
            
            # Draw lines
            ax1.plot([sx0, sx1], [sy0, sy1], color=color_ax1, linewidth=cur_lw_ax1, alpha=alpha_ax1, zorder=z_ax1)
            ax2.plot(wx, wy, color="#B91F1F", linewidth=lw, alpha=0.9, zorder=2)

    # Set fixed framing
    ax1.set_xlim(left=-1.0, right=1.0)
    ax1.set_ylim(bottom=-1.0, top=1.0)
    ax2.set_xlim(left=-1.0, right=1.0)
    ax2.set_ylim(bottom=-1.0, top=1.0)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{filename}.svg"
    plt.savefig(out_path, format="svg", bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated: {out_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratio", type=float, default=16.0, help="Scale factor per recursion")
    parser.add_argument("--turns", type=float, default=1.0, help="Twist turns per recursion")
    parser.add_argument("--grid", type=int, default=16, help="Grid divisions per outer square")
    parser.add_argument("--recursions", type=int, default=3, help="Number of recursions")
    parser.add_argument("--out", type=str, default="3b1b_original_escher_grid", help="Output filename")
    parser.add_argument("--image", type=str, default=None, help="Input image to map")
    args = parser.parse_args()
    
    draw_3b1b_escher_grid(
        filename=args.out, 
        ratio=args.ratio, 
        extra_turns=args.turns,
        grid_size=args.grid,
        recursions=args.recursions,
        image_path=args.image
    )
