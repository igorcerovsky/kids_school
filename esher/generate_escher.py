"""
Escher / Droste Conformal Grid Worksheet Generator (Pure SVG Vector Output)
===========================================================================
Based on the mathematical structure described by de Smit & Lenstra (AMS Notices 2003)
and the Jos Leys implementation (josleys.com/article_show.php?id=82).

The core conformal map:   w = (z/r1)^β
where β = f·exp(iα), α = arctan(log(r2/r1) / 2π), f = cos(α)

This script generates a printable A3-landscape worksheet containing:
  Left panel  – nested self-similar regular square grid (vector)
  Right panel – same grid warped conformally into an Escher spiral (vector)

Both panels are rendered as pure SVG vector graphics for infinite zooming.
"""

import argparse
import cmath
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output_escher"
DPI        = 150

COL_BG        = "#FDFCF7"
COL_IMAGE_BG  = "#FFFFFF"

# Grid colors
COL_MAJ_SRC = (30,  100, 195)   # strong blue – major lines
COL_MIN_SRC = (160, 200, 240)   # light blue  – minor lines
COL_MAJ_DST = (185,  40,  30)   # strong red  – major lines
COL_MIN_DST = (235, 160, 150)   # salmon      – minor lines


# ─────────────────────────────────────────────────────────────────────────────
# ESCHER / DROSTE CONFORMAL MAP
# ─────────────────────────────────────────────────────────────────────────────

class EscherMap:
    """Encapsulates the Droste/Escher conformal map parameters."""

    def __init__(self, r1: float = 0.1, r2: float = 1.0,
                 extra_turns: float = 0.0):
        self.r1 = r1
        self.r2 = r2
        ratio = r2 / r1
        log_ratio       = math.log(ratio)
        self.alpha      = math.atan(log_ratio / (2 * math.pi))
        self.f          = math.cos(self.alpha)
        self.beta       = self.f * cmath.exp(1j * self.alpha)
        self.inv_beta   = 1.0 / self.beta
        self.log_ratio  = log_ratio
        self.strip_h    = 2 * math.pi
        self.extra_turns = extra_turns

        zoom_complex     = (ratio + 0j) ** self.beta
        self.zoom_factor = abs(zoom_complex)
        self.zoom_angle  = cmath.phase(zoom_complex)

    def forward(self, z_complex: np.ndarray) -> np.ndarray:
        """Forward map: source z → destination w."""
        z_safe = np.where(np.abs(z_complex) < 1e-12, 1e-12 + 0j, z_complex)
        log_z = np.log(z_safe)
        if self.extra_turns != 0:
            log_z = log_z + 1j * self.extra_turns * np.real(log_z) / self.log_ratio * 2 * math.pi
        return np.exp(self.beta * log_z)


# ─────────────────────────────────────────────────────────────────────────────
# IMAGE WARPING UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def bilinear_sample(img_arr: np.ndarray, px: np.ndarray, py: np.ndarray) -> np.ndarray:
    """
    Bilinear interpolation of img_arr at coordinate matrices (px, py).
    img_arr shape: (H, W, C)
    px, py shape: (H_out, W_out)
    """
    H, W, C = img_arr.shape
    px = np.clip(px, 0, W - 1 - 1e-9)
    py = np.clip(py, 0, H - 1 - 1e-9)

    x0 = np.floor(px).astype(np.int32)
    x1 = x0 + 1
    y0 = np.floor(py).astype(np.int32)
    y1 = y0 + 1

    # Weights
    wa = (x1 - px) * (y1 - py)
    wb = (px - x0) * (y1 - py)
    wc = (x1 - px) * (py - y0)
    wd = (px - x0) * (py - y0)

    # Expand dimensions for multiplication with RGB channels
    wa = wa[..., np.newaxis]
    wb = wb[..., np.newaxis]
    wc = wc[..., np.newaxis]
    wd = wd[..., np.newaxis]

    # Sample pixels
    sampled = (wa * img_arr[y0, x0] +
               wb * img_arr[y0, x1] +
               wc * img_arr[y1, x0] +
               wd * img_arr[y1, x1])
    return sampled


def warp_image_conformal(img_array: np.ndarray, emap: EscherMap, width: int = 1200, height: int = 1200) -> np.ndarray:
    """
    Warps the input img_array using the inverse of the Escher conformal map.
    """
    # Create coordinate grid in the destination w plane: [-1, 1]x[-1, 1]
    x = np.linspace(-1.0, 1.0, width)
    y = np.linspace(1.0, -1.0, height) # Y-axis starts from top (inverted pixel coords)
    xx, yy = np.meshgrid(x, y)
    w = xx + 1j * yy

    # Phase and modulus
    mod_w = np.abs(w)
    phase_w = np.angle(w)
    # Avoid log(0)
    mod_w = np.maximum(mod_w, 1e-12)
    log_w = np.log(mod_w) + 1j * phase_w

    # Inverse map to log-coordinate s = log(w) / beta
    s = log_w / emap.beta
    u = np.real(s)
    v = np.imag(s)

    # Adjust imaginary part if extra_turns are specified
    if emap.extra_turns != 0:
        v = v - emap.extra_turns * (u / emap.log_ratio) * (2 * np.pi)

    # Convert back to unscaled complex coordinates z = exp(u + i*v)
    z_unscaled = np.exp(u + 1j * v)

    # Map each z to the main tile (annulus: r1 < Chebyshev_norm <= r2)
    # Chebyshev norm N = max(|x|, |y|)
    N = np.maximum(np.abs(np.real(z_unscaled)), np.abs(np.imag(z_unscaled)))
    N_safe = np.maximum(N, 1e-12)

    # Calculate scaling factor power
    k = np.floor(-np.log(N_safe) / emap.log_ratio)
    
    # Scale coordinates back to tile 0 (main annulus)
    ratio = emap.r2 / emap.r1
    z_scaled = z_unscaled * (ratio ** k)

    # Convert z_scaled back to pixel coordinates in the source image
    # Source image represents the square [-1, 1]x[-1, 1]
    src_h, src_w, src_c = img_array.shape
    px = (np.real(z_scaled) + 1.0) * 0.5 * (src_w - 1)
    py = (1.0 - np.imag(z_scaled)) * 0.5 * (src_h - 1)

    # Bilinear sampling
    warped_img = bilinear_sample(img_array, px, py)
    
    # Force the exact center (origin) mapping to white
    origin_mask = (np.abs(w) < 1e-10)
    warped_img[origin_mask] = 255.0

    return warped_img.astype(np.uint8)


def create_nested_image(img_array: np.ndarray, emap: EscherMap, width: int = 1200, height: int = 1200) -> np.ndarray:
    """
    Create the self-similar nested image for the left panel using mathematical
    Chebyshev-norm tiling.  Every pixel in [-1,1]^2 is scaled back to the
    primary annulus (r1 < max(|x|,|y|) <= 1.0) and sampled from the source
    image, producing a continuous, seamless recursive pattern.
    """
    x = np.linspace(-1.0, 1.0, width)
    y = np.linspace(1.0, -1.0, height)
    xx, yy = np.meshgrid(x, y)

    # Chebyshev norm N = max(|x|, |y|)
    N = np.maximum(np.abs(xx), np.abs(yy))
    N_safe = np.maximum(N, 1e-12)

    ratio = emap.r2 / emap.r1

    # Scale each point back into the primary annulus
    k = np.floor(-np.log(N_safe) / emap.log_ratio)
    xx_scaled = xx * (ratio ** k)
    yy_scaled = yy * (ratio ** k)

    # Map to source image pixel coordinates
    src_h, src_w, _ = img_array.shape
    px = (xx_scaled + 1.0) * 0.5 * (src_w - 1)
    py = (1.0 - yy_scaled) * 0.5 * (src_h - 1)

    nested_img = bilinear_sample(img_array, px, py)
    return nested_img.astype(np.uint8)


# ─────────────────────────────────────────────────────────────────────────────
# NESTED REGULAR GRID DRAWING (VECTOR)
# ─────────────────────────────────────────────────────────────────────────────

def plot_labels_nested_regular(ax, n_major, col_major_hex):
    """Draw A/B/C… column and 1/2/3… row labels on the nested regular grid."""
    cell_size = 2.0 / (2 * n_major)
    
    # Column labels (A, B, C...) at the top (y ≈ 1.05)
    for col in range(2 * n_major):
        x = -1.0 + (col + 0.5) * cell_size
        ax.text(x, 1.03, chr(ord('A') + col % 26),
                color=col_major_hex, ha="center", va="bottom", fontsize=10, fontweight="bold")
                
    # Row labels (1, 2, 3...) at the left (x ≈ -1.05)
    for row in range(2 * n_major):
        y = 1.0 - (row + 0.5) * cell_size
        ax.text(-1.03, y, str(row + 1),
                color=col_major_hex, ha="right", va="center", fontsize=10, fontweight="bold")


def plot_nested_grid_vector(ax, n_major, n_minor, ratio, depth_levels):
    """Draw the nested self-similar square grid on a matplotlib axis using vector lines."""
    col_maj = "#1E64C3"
    col_min = "#A0C8F0"
    
    geom_scale = 2.0
    
    # We ignore depth_levels and generate enough levels to cover the space
    for level in range(-6, 24):
        scale = geom_scale ** (-level)
        r2 = 1.0 * scale
        r1 = r2 / geom_scale
        
        if r2 < 0.002: # too small to be visible
            continue
            
        step_maj = r2 / n_major
        step_min = r2 / (n_major * n_minor)
        
        # Scale line widths non-linearly based on the scale factor (tighter lines are thinner)
        lw_factor = scale ** 0.35
        lw_maj = max(1.5 * lw_factor, 0.15)
        lw_min = max(0.7 * lw_factor, 0.07)
        
        level_step = max(1, int(round(math.log(ratio) / math.log(geom_scale))))
        is_base = (level == 0 or level == level_step)

        # Helper to plot a segment
        def plot_seg(x0, y0, x1, y1, color, width, is_thick=False):
            z = 4 if is_thick else (2 if width > 1.0 else 1)
            c = "#27AE60" if is_thick else color
            ax.plot([x0, x1], [y0, y1], color=c, linewidth=width, zorder=z)

        # 1. Minor lines
        n_total = n_major * n_minor
        for col in range(-n_total, n_total + 1):
            if col % n_minor == 0:
                continue
            x = col * step_min
            if abs(x) >= r1 - 1e-9:
                plot_seg(x, -r2, x, r2, col_min, lw_min)
            else:
                plot_seg(x, -r2, x, -r1, col_min, lw_min)
                plot_seg(x, r1, x, r2, col_min, lw_min)
                
        for row in range(-n_total, n_total + 1):
            if row % n_minor == 0:
                continue
            y = row * step_min
            if abs(y) >= r1 - 1e-9:
                plot_seg(-r2, y, r2, y, col_min, lw_min)
            else:
                plot_seg(-r2, y, -r1, y, col_min, lw_min)
                plot_seg(r1, y, r2, y, col_min, lw_min)
                
        # 2. Major lines
        for col in range(-n_major, n_major + 1):
            x = col * step_maj
            is_thick = is_base and abs(col) == n_major
            cur_lw = lw_maj * 2.5 if is_thick else lw_maj
            if abs(x) >= r1 - 1e-9:
                plot_seg(x, -r2, x, r2, col_maj, cur_lw, is_thick)
            else:
                plot_seg(x, -r2, x, -r1, col_maj, cur_lw, is_thick)
                plot_seg(x, r1, x, r2, col_maj, cur_lw, is_thick)
                
        for row in range(-n_major, n_major + 1):
            y = row * step_maj
            is_thick = is_base and abs(row) == n_major
            cur_lw = lw_maj * 2.5 if is_thick else lw_maj
            if abs(y) >= r1 - 1e-9:
                plot_seg(-r2, y, r2, y, col_maj, cur_lw, is_thick)
            else:
                plot_seg(-r2, y, -r1, y, col_maj, cur_lw, is_thick)
                plot_seg(r1, y, r2, y, col_maj, cur_lw, is_thick)


# ─────────────────────────────────────────────────────────────────────────────
# NESTED ESCHER GRID DRAWING (VECTOR)
# ─────────────────────────────────────────────────────────────────────────────

def plot_labels_nested_escher(ax, n_major, emap, col_major_hex):
    """Draw grid-cell reference labels (A/B/C…, 1/2/3…) on the warped nested grid."""
    ratio = emap.r2 / emap.r1

    # Helper to check if cell center is in tile 0 (the active square annulus)
    def is_in_tile0(col, row):
        u_c = (col + 0.5) / (2 * n_major)
        v_c = (row + 0.5) / (2 * n_major)
        return max(abs(u_c - 0.5), abs(v_c - 0.5)) >= 0.5 / ratio

    # Column labels (A, B, C...) at topmost visible edge of tile 0
    for col in range(2 * n_major):
        row_top = None
        for r in range(2 * n_major):
            if is_in_tile0(col, r):
                row_top = r
                break
        if row_top is not None:
            u_c = (col + 0.5) / (2 * n_major)
            v_c = (row_top + 0.25) / (2 * n_major)
            
            x_target = (u_c - 0.5) * 2.0 * emap.r2
            y_target = (0.5 - v_c) * 2.0 * emap.r2
            z_target = x_target + 1j * y_target
            
            w_label = emap.forward(z_target)
            w_real = np.real(w_label)
            w_imag = np.imag(w_label)
            if -0.98 <= w_real <= 0.98 and -0.98 <= w_imag <= 0.98:
                ax.text(w_real, w_imag, chr(ord('A') + col % 26),
                        color=col_major_hex, ha="center", va="center", fontsize=10, fontweight="bold",
                        clip_on=True)

    # Row labels (1, 2, 3...) at leftmost visible edge of tile 0
    for row in range(2 * n_major):
        col_left = None
        for c in range(2 * n_major):
            if is_in_tile0(c, row):
                col_left = c
                break
        if col_left is not None:
            u_c = (col_left + 0.25) / (2 * n_major)
            v_c = (row + 0.5) / (2 * n_major)
            
            x_target = (u_c - 0.5) * 2.0 * emap.r2
            y_target = (0.5 - v_c) * 2.0 * emap.r2
            z_target = x_target + 1j * y_target
            
            w_label = emap.forward(z_target)
            w_real = np.real(w_label)
            w_imag = np.imag(w_label)
            if -0.98 <= w_real <= 0.98 and -0.98 <= w_imag <= 0.98:
                ax.text(w_real, w_imag, str(row + 1),
                        color=col_major_hex, ha="center", va="center", fontsize=10, fontweight="bold",
                        clip_on=True)


def plot_nested_escher_grid_vector(ax, n_major, n_minor, emap, depth_levels):
    """Draw the warped nested grid on a matplotlib axis using vector curves."""
    col_maj = "#B91F1F" # strong red
    col_min = "#EBA096" # salmon
    
    geom_scale = 2.0
    
    # We ignore depth_levels and generate enough levels to cover the space
    for level in range(-6, 24):
        scale = geom_scale ** (-level)
        r2 = 1.0 * scale
        r1 = r2 / geom_scale
        
        if r2 < 0.002: # too small to be visible
            continue
            
        step_maj = r2 / n_major
        step_min = r2 / (n_major * n_minor)
        
        # Scale line widths non-linearly based on the scale factor (tighter lines are thinner)
        lw_factor = scale ** 0.35
        lw_maj = max(1.5 * lw_factor, 0.15)
        lw_min = max(0.7 * lw_factor, 0.07)

        # Helper to generate un-torn curves using angle unwrapping
        def plot_warped_line(x0, y0, x1, y1, color, width):
            pts_z = np.linspace(x0 + 1j*y0, x1 + 1j*y1, 200)
            
            r = np.abs(pts_z)
            theta = np.unwrap(np.angle(pts_z))
            
            log_z = np.log(np.maximum(r, 1e-12)) + 1j * theta
            if emap.extra_turns != 0:
                log_z = log_z + 1j * emap.extra_turns * np.real(log_z) / emap.log_ratio * 2 * math.pi
                
            pts_w = np.exp(emap.beta * log_z)
            
            # Let Matplotlib handle clipping perfectly
            ax.plot(np.real(pts_w), np.imag(pts_w), color=color, linewidth=width, zorder=2 if width > 1.0 else 1)

        # 1. Minor lines
        n_total = n_major * n_minor
        for col in range(-n_total, n_total + 1):
            if col % n_minor == 0:
                continue
            x = col * step_min
            if abs(x) >= r1 - 1e-9:
                plot_warped_line(x, -r2, x, r2, col_min, lw_min)
            else:
                plot_warped_line(x, -r2, x, -r1, col_min, lw_min)
                plot_warped_line(x, r1, x, r2, col_min, lw_min)
                
        for row in range(-n_total, n_total + 1):
            if row % n_minor == 0:
                continue
            y = row * step_min
            if abs(y) >= r1 - 1e-9:
                plot_warped_line(-r2, y, r2, y, col_min, lw_min)
            else:
                plot_warped_line(-r2, y, -r1, y, col_min, lw_min)
                plot_warped_line(r1, y, r2, y, col_min, lw_min)
                
        # 2. Major lines
        for col in range(-n_major, n_major + 1):
            x = col * step_maj
            if abs(x) >= r1 - 1e-9:
                plot_warped_line(x, -r2, x, r2, col_maj, lw_maj)
            else:
                plot_warped_line(x, -r2, x, -r1, col_maj, lw_maj)
                plot_warped_line(x, r1, x, r2, col_maj, lw_maj)
                
        for row in range(-n_major, n_major + 1):
            y = row * step_maj
            if abs(y) >= r1 - 1e-9:
                plot_warped_line(-r2, y, r2, y, col_maj, lw_maj)
            else:
                plot_warped_line(-r2, y, -r1, y, col_maj, lw_maj)
                plot_warped_line(r1, y, r2, y, col_maj, lw_maj)


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET COMPOSER
# ─────────────────────────────────────────────────────────────────────────────

def make_worksheet(emap: EscherMap,
                   n_major: int,
                   n_minor: int,
                   preset_name: str,
                   img_array: np.ndarray = None,
                   blank: bool = False) -> plt.Figure:
    """Compose the worksheet showing the regular nested grid (with image) and warped grid (with warped image or blank)."""
    fig = plt.figure(figsize=(16.5, 11.7))
    fig.patch.set_facecolor(COL_BG)

    depth_levels_l = range(0, 8)
    depth_levels_r = range(-1, 8)

    left_title  = "Vorlage – Quadratisches nested Gitter"
    right_title = "Hier zeichnen – Konform verzerrte Spirale"

    # Left panel: regular grid
    ax_l = fig.add_axes([0.02, 0.06, 0.46, 0.83])
    ax_l.set_aspect("equal")
    ax_l.set_xlim(-1.0, 1.0)
    ax_l.set_ylim(-1.0, 1.0)
    
    # White background behind the left image & grid
    bg_l = mpatches.Rectangle((-1.0, -1.0), 2.0, 2.0, facecolor=COL_IMAGE_BG, zorder=0)
    ax_l.add_patch(bg_l)
    
    if img_array is not None:
        # Create a continuous self-similar image via mathematical tiling
        nested_img = create_nested_image(img_array, emap, 1200, 1200)
        ax_l.imshow(nested_img, extent=[-1.0, 1.0, -1.0, 1.0], zorder=1)
            
    plot_nested_grid_vector(ax_l, n_major, n_minor, emap.r2 / emap.r1, depth_levels_l)
    plot_labels_nested_regular(ax_l, n_major, "#1E64C3")
    ax_l.axis("off")
    ax_l.set_title(left_title, fontsize=14, fontweight="bold",
                   color="#1E64C3", pad=8)

    # Right panel: warped grid
    ax_r = fig.add_axes([0.52, 0.06, 0.46, 0.83])
    ax_r.set_aspect("equal")
    ax_r.set_xlim(-1.0, 1.0)
    ax_r.set_ylim(-1.0, 1.0)
    
    # White background behind the right image & grid
    bg_r = mpatches.Rectangle((-1.0, -1.0), 2.0, 2.0, facecolor=COL_IMAGE_BG, zorder=0)
    ax_r.add_patch(bg_r)
    
    if img_array is not None and not blank:
        # Warp and draw image
        warped_img = warp_image_conformal(img_array, emap, 1200, 1200)
        ax_r.imshow(warped_img, extent=[-1.0, 1.0, -1.0, 1.0], zorder=1)
        
    plot_nested_escher_grid_vector(ax_r, n_major, n_minor, emap, depth_levels_r)
    plot_labels_nested_escher(ax_r, n_major, emap, "#B91F1F")
    
    # Add a border around the right panel to match the left square's boundary
    border = mpatches.Rectangle((-1.0, -1.0), 2.0, 2.0, fill=False, edgecolor="#B91F1F", linewidth=1.5, zorder=3)
    ax_r.add_patch(border)
    
    ax_r.axis("off")
    ax_r.set_title(right_title, fontsize=14, fontweight="bold",
                   color="#B91F1F", pad=8)

    rot_deg   = round(math.degrees(abs(emap.zoom_angle)), 1)
    ratio_val = round(emap.r2 / emap.r1, 1)
    info_str  = (f"r₂/r₁ = {ratio_val:.0f}  │  "
                 f"Zoom ×{emap.zoom_factor:.2f}  │  "
                 f"Drehung {rot_deg}°  │  "
                 f"Raster {n_major * 2}×{n_major * 2} (÷{n_minor})")

    title       = "Escher / Droste-Spirale Gittermodell"
    subtitle    = (f"Übertrage deine Zeichnung aus dem blauen Raster in das "
                   f"entsprechende rote Spiralfeld.   {info_str}")

    fig.text(0.5, 0.975, title, ha="center", va="top", fontsize=22, fontweight="bold", color="#1A1A2E")
    fig.text(0.5, 0.925, subtitle, ha="center", va="top", fontsize=10, color="#444466", style="italic")

    patches = [
        mpatches.Patch(color=tuple(c/255 for c in COL_MAJ_SRC), label=f"Hauptlinien (je {n_major * 2} Felder)"),
        mpatches.Patch(color=tuple(c/255 for c in COL_MIN_SRC), label=f"Hilfslinien (÷{n_minor} pro Feld)"),
        mpatches.Patch(color=tuple(c/255 for c in COL_MAJ_DST), label="Escher-Spirale Hauptlinien"),
        mpatches.Patch(color=tuple(c/255 for c in COL_MIN_DST), label="Escher-Spirale Hilfslinien"),
    ]
    fig.legend(handles=patches, loc="lower center", ncol=4, fontsize=9, framealpha=0.8, bbox_to_anchor=(0.5, 0.005))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# PRESETS  (r2/r1 ratio → controls spiral tightness)
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = {
    "escher":  dict(ratio=256, extra_turns=0.0, grid=8),  # Lenstra's exact Escher ratio
    "tight":   dict(ratio=16,  extra_turns=0.0, grid=8),  # more spiral turns
    "loose":   dict(ratio=8,   extra_turns=0.0, grid=8),  # gentler, good for beginners
    "gentle":  dict(ratio=4,   extra_turns=0.0, grid=4),  # very gentle – small kids
    "twisted": dict(ratio=16,  extra_turns=0.5, grid=8),  # extra spiral twist
}


def main():
    parser = argparse.ArgumentParser(description="Generate Escher/Droste conformal grid worksheets as SVG vectors.")
    parser.add_argument("--grid", type=int, default=None, help="Number of MAJOR grid cells per half-side (default: auto from preset)")
    parser.add_argument("--minor", type=int, default=4, help="Minor sub-divisions per major cell (default: 4)")
    parser.add_argument("--ratio", type=float, default=None, help="r2/r1 ratio (overrides preset)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default=None, help="Named parameter preset (default: all presets)")
    parser.add_argument("--spiral-turns", type=float, default=0.0, help="Extra spiral twist (default: 0)")
    parser.add_argument("--image", type=str, default=None, help="Path to an input image to apply the conformal map to")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    img_array = None
    img_name = "grid"
    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image path {image_path} does not exist.")
            return
        try:
            with Image.open(image_path) as img:
                img_rgb = img.convert("RGB")
                img_array = np.array(img_rgb)
                img_name = image_path.stem
                print(f"Loaded image: {image_path.name} ({img_rgb.size[0]}x{img_rgb.size[1]})")
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return

    if args.ratio is not None:
        presets = {"custom": dict(ratio=args.ratio,
                                  extra_turns=args.spiral_turns,
                                  grid=args.grid if args.grid else 8)}
    elif args.preset:
        presets = {args.preset: PRESETS[args.preset]}
    else:
        presets = PRESETS

    n_minor = args.minor

    print(f"\n{'='*68}")
    print(f"  Escher / Droste Vector Grid Generator")
    print(f"  Output: {OUTPUT_DIR.resolve()}")
    print(f"{'='*68}\n")

    for preset_name, params in presets.items():
        r2    = 1.0
        r1    = r2 / params["ratio"]
        emap  = EscherMap(r1=r1, r2=r2,
                          extra_turns=params["extra_turns"])
        
        # Determine n_major for this run
        if args.grid is not None:
            n_major = args.grid
        else:
            n_major = params.get("grid", 8)

        if img_array is not None:
            # Generate two sheets: full (solved) and blank (for drawing)
            # 1. Full/Solved sheet
            stem = f"{img_name}_{preset_name}_g{n_major}m{n_minor}"
            print(f"  [{preset_name} with image]  "
                  f"ratio={params['ratio']:.0f}  "
                  f"grid {n_major * 2}x{n_major * 2}  "
                  f"…", end="", flush=True)

            fig = make_worksheet(emap, n_major, n_minor, preset_name, img_array=img_array, blank=False)
            for ext in ("svg", "png", "pdf"):
                fig.savefig(OUTPUT_DIR / f"{stem}.{ext}", dpi=DPI,
                            bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
            print(" (full ✓)", end="", flush=True)

            # 2. Blank sheet
            stem_blank = f"{img_name}_{preset_name}_g{n_major}m{n_minor}_blank"
            fig_blank = make_worksheet(emap, n_major, n_minor, preset_name, img_array=img_array, blank=True)
            for ext in ("svg", "png", "pdf"):
                fig_blank.savefig(OUTPUT_DIR / f"{stem_blank}.{ext}", dpi=DPI,
                            bbox_inches="tight", facecolor=fig_blank.get_facecolor())
            plt.close(fig_blank)
            print(" (blank ✓)  ✓")
        else:
            stem  = f"grid_{preset_name}_g{n_major}m{n_minor}"
            print(f"  [{preset_name}]  "
                  f"ratio={params['ratio']:.0f}  "
                  f"α={math.degrees(emap.alpha):.1f}°  "
                  f"zoom×{emap.zoom_factor:.2f}  "
                  f"rot {math.degrees(emap.zoom_angle):.1f}°  "
                  f"grid {n_major * 2}x{n_major * 2}  "
                  f"…", end="", flush=True)

            fig = make_worksheet(emap, n_major, n_minor, preset_name, img_array=None, blank=True)
            # Save as SVG, PDF, and PNG
            for ext in ("svg", "png", "pdf"):
                fig.savefig(OUTPUT_DIR / f"{stem}.{ext}", dpi=DPI,
                            bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
            print("  ✓")

    total = len(presets)
    print(f"\n  Done! {total} worksheets → {OUTPUT_DIR.resolve()}\n")


if __name__ == "__main__":
    main()
