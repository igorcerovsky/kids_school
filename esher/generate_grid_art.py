"""
Escher Grid Drawing Generator
==============================
Generates printable worksheets for kids:
  - Left panel:  source image with a regular square grid
  - Right panel: same image warped + the corresponding distorted grid

Kids copy each grid cell from the regular side onto the distorted side,
learning observation skills, drawing, and spatial geometry.

Usage
-----
  # Generate all distortions with the built-in 'house' drawing
  python generate_grid_art.py

  # Pick a different built-in image
  python generate_grid_art.py --builtin fish

  # Use your own image file
  python generate_grid_art.py --image my_photo.png

  # One specific distortion only
  python generate_grid_art.py --distortion polar

  # Control grid density (default 8×8)
  python generate_grid_art.py --grid 10
"""

import argparse
import math
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image, ImageDraw

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output"
IMG_SIZE   = 512          # source image is rendered at this square size (px)
DPI        = 150          # output resolution

# Colour palette
COL_BG        = "#FDFCF7"   # warm off-white page
COL_GRID_SRC  = "#4A90D9"   # regular grid colour
COL_GRID_DIST = "#E07B3A"   # distorted grid colour
COL_IMAGE_BG  = "#FFFFFF"   # image background
COL_DRAW_INK  = "#1A1A2E"   # ink for built-in drawings

# ─────────────────────────────────────────────────────────────────────────────
# BUILT-IN LINE-ART IMAGES
# ─────────────────────────────────────────────────────────────────────────────
def _draw_house(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Simple house: walls, roof, door, two windows."""
    m = w // 10          # margin
    bw, bh = w - 2*m, h - 2*m   # body width/height

    # Ground floor rectangle
    rx0, ry0 = m, h//2
    rx1, ry1 = w - m, h - m
    draw.rectangle([rx0, ry0, rx1, ry1], outline=COL_DRAW_INK, width=4)

    # Roof triangle
    roof_peak = (w//2, m + h//10)
    draw.polygon([rx0, ry0, rx1, ry0, roof_peak], outline=COL_DRAW_INK, width=4)

    # Door (centered, bottom)
    dw, dh = bw//5, bh//3
    dx0 = w//2 - dw//2
    dy0 = ry1 - dh
    draw.rectangle([dx0, dy0, dx0+dw, ry1], outline=COL_DRAW_INK, width=3)
    # Door knob
    draw.ellipse([dx0+dw-12, (dy0+ry1)//2-5, dx0+dw-4, (dy0+ry1)//2+5],
                 fill=COL_DRAW_INK)

    # Left window
    wx, wy = rx0 + bw//5 - dw//2, ry0 + bh//8
    draw.rectangle([wx, wy, wx+dw, wy+dw], outline=COL_DRAW_INK, width=3)
    draw.line([wx, wy+dw//2, wx+dw, wy+dw//2], fill=COL_DRAW_INK, width=2)
    draw.line([wx+dw//2, wy, wx+dw//2, wy+dw], fill=COL_DRAW_INK, width=2)

    # Right window (mirror)
    wx2 = rx1 - bw//5 - dw//2
    draw.rectangle([wx2, wy, wx2+dw, wy+dw], outline=COL_DRAW_INK, width=3)
    draw.line([wx2, wy+dw//2, wx2+dw, wy+dw//2], fill=COL_DRAW_INK, width=2)
    draw.line([wx2+dw//2, wy, wx2+dw//2, wy+dw], fill=COL_DRAW_INK, width=2)

    # Chimney
    cw = dw // 2
    cx = roof_peak[0] + bw//8
    draw.rectangle([cx, m + h//10 - h//6, cx+cw, ry0], outline=COL_DRAW_INK, width=3)


def _draw_fish(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Simple fish silhouette with eye, fin, tail."""
    cx, cy = w // 2, h // 2
    rx, ry = int(w * 0.30), int(h * 0.22)

    # Body ellipse
    draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=COL_DRAW_INK, width=4)

    # Tail (triangle to the left)
    tx = cx - rx
    draw.polygon([(tx, cy),
                  (tx - int(rx*0.7), cy - ry),
                  (tx - int(rx*0.7), cy + ry)],
                 outline=COL_DRAW_INK, width=4)

    # Eye
    ex = cx + int(rx * 0.5)
    er = max(int(min(rx, ry) * 0.12), 6)
    draw.ellipse([ex-er, cy-er, ex+er, cy+er], fill=COL_DRAW_INK)

    # Dorsal fin
    fx0 = cx - int(rx*0.1)
    draw.polygon([(fx0, cy - ry),
                  (fx0 - int(rx*0.2), cy - ry - int(ry*0.6)),
                  (fx0 + int(rx*0.3), cy - ry)],
                 outline=COL_DRAW_INK, width=3)

    # Mouth
    draw.arc([cx+int(rx*0.75)-10, cy-8, cx+int(rx*0.75)+10, cy+8],
             start=0, end=180, fill=COL_DRAW_INK, width=3)

    # Scales (3 arcs)
    for i in range(3):
        scx = cx - int(rx*0.2) + i * int(rx*0.25)
        scy = cy
        sr  = int(ry * 0.35)
        draw.arc([scx-sr, scy, scx+sr, scy+sr*2], start=180, end=360,
                 fill=COL_DRAW_INK, width=2)


def _draw_star(draw: ImageDraw.ImageDraw, w: int, h: int):
    """5-pointed star with an inner circle."""
    cx, cy   = w // 2, h // 2
    R_outer  = int(min(w, h) * 0.42)
    R_inner  = int(R_outer * 0.42)
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = R_outer if i % 2 == 0 else R_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, outline=COL_DRAW_INK, width=4)

    # Inner circle
    cr = int(R_inner * 0.55)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=COL_DRAW_INK, width=3)

    # Radial lines from centre to each inner vertex
    for i in range(1, 10, 2):
        draw.line([cx, cy, int(pts[i][0]), int(pts[i][1])],
                  fill=COL_DRAW_INK, width=2)


def _draw_face(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Simple smiley/friendly face."""
    cx, cy = w // 2, h // 2
    R = int(min(w, h) * 0.42)

    # Head outline
    draw.ellipse([cx-R, cy-R, cx+R, cy+R], outline=COL_DRAW_INK, width=5)

    # Eyes
    ex_off = int(R * 0.32)
    ey_off = int(R * 0.22)
    er     = int(R * 0.10)
    for sign in (-1, 1):
        ex = cx + sign * ex_off
        ey = cy - ey_off
        draw.ellipse([ex-er, ey-er, ex+er, ey+er], fill=COL_DRAW_INK)
        # Eyebrow
        bx0 = ex - int(er*1.4)
        bx1 = ex + int(er*1.4)
        by  = ey - int(er*2.0)
        draw.arc([bx0, by - er//2, bx1, by + er//2], start=0, end=180,
                 fill=COL_DRAW_INK, width=3)

    # Nose
    nose_pts = [(cx, cy - int(R*0.05)),
                (cx - int(R*0.08), cy + int(R*0.15)),
                (cx + int(R*0.08), cy + int(R*0.15))]
    draw.polygon(nose_pts, outline=COL_DRAW_INK, width=2)

    # Smile
    sm_r = int(R * 0.38)
    draw.arc([cx - sm_r, cy + int(R*0.05), cx + sm_r, cy + int(R*0.55)],
             start=10, end=170, fill=COL_DRAW_INK, width=4)

    # Ears
    ear_r = int(R * 0.15)
    for sign in (-1, 1):
        ex = cx + sign * R
        draw.ellipse([ex - ear_r, cy - ear_r, ex + ear_r, cy + ear_r],
                     outline=COL_DRAW_INK, width=4)

    # Hair tufts
    for angle_deg in range(-80, 81, 20):
        a = math.radians(angle_deg - 90)
        hx = int(cx + R * math.cos(a))
        hy = int(cy + R * math.sin(a))
        ex2 = int(cx + (R + int(R*0.18)) * math.cos(a))
        ey2 = int(cy + (R + int(R*0.18)) * math.sin(a))
        draw.line([hx, hy, ex2, ey2], fill=COL_DRAW_INK, width=3)


def _draw_rocket(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Simple rocket ship."""
    cx = w // 2
    m  = w // 10

    # Body rectangle
    bw, bh = w // 3, int(h * 0.45)
    bx0 = cx - bw//2
    bx1 = cx + bw//2
    by0 = int(h * 0.2)
    by1 = by0 + bh
    draw.rectangle([bx0, by0, bx1, by1], outline=COL_DRAW_INK, width=4)

    # Nose cone (triangle)
    draw.polygon([(cx, m), (bx0, by0), (bx1, by0)],
                 outline=COL_DRAW_INK, width=4)

    # Porthole
    pr = bw // 5
    draw.ellipse([cx-pr, by0 + bh//4 - pr, cx+pr, by0 + bh//4 + pr],
                 outline=COL_DRAW_INK, width=3)

    # Left fin
    draw.polygon([(bx0, by1 - bh//3),
                  (bx0 - bw//2, by1),
                  (bx0, by1)], outline=COL_DRAW_INK, width=3)

    # Right fin
    draw.polygon([(bx1, by1 - bh//3),
                  (bx1 + bw//2, by1),
                  (bx1, by1)], outline=COL_DRAW_INK, width=3)

    # Exhaust flames
    for i in range(4):
        fx = bx0 + (i + 0.5) * bw // 4
        fh = int(h * 0.08 + h * 0.06 * (i % 2))
        draw.ellipse([int(fx)-6, by1, int(fx)+6, by1 + fh],
                     outline=COL_DRAW_INK, width=2)


BUILTIN_IMAGES = {
    "house":  _draw_house,
    "fish":   _draw_fish,
    "star":   _draw_star,
    "face":   _draw_face,
    "rocket": _draw_rocket,
}


def make_builtin_image(name: str, size: int = IMG_SIZE) -> Image.Image:
    """Return a white PIL image with the requested built-in drawing."""
    img  = Image.new("RGB", (size, size), COL_IMAGE_BG)
    draw = ImageDraw.Draw(img)
    BUILTIN_IMAGES[name](draw, size, size)
    return img


# ─────────────────────────────────────────────────────────────────────────────
# DISTORTION FUNCTIONS
# Each function takes (x_norm, y_norm) arrays in [0,1]×[0,1] and returns
# (x_src, y_src) arrays in [0,1]×[0,1] — the inverse mapping:
# "where does the pixel in the distorted image come from in the source?"
# ─────────────────────────────────────────────────────────────────────────────

def _warp_polar(xn: np.ndarray, yn: np.ndarray):
    """Rectangular → polar (top of image maps to centre of a disc)."""
    # theta in [0, 2π], r in [0, 1]
    theta = xn * 2 * np.pi
    r     = yn           # r=0 at top row → centre; r=1 at bottom → edge
    cx = 0.5 + r * 0.5 * np.cos(theta - np.pi/2)
    cy = 0.5 + r * 0.5 * np.sin(theta - np.pi/2)
    return cx, cy


def _warp_fisheye(xn: np.ndarray, yn: np.ndarray, strength: float = 0.6):
    """Barrel (fisheye) distortion — centre bulges outward."""
    dx = xn - 0.5
    dy = yn - 0.5
    r2 = dx**2 + dy**2
    factor = 1.0 + strength * r2 * 4
    return 0.5 + dx / factor, 0.5 + dy / factor


def _warp_perspective(xn: np.ndarray, yn: np.ndarray):
    """Trapezoidal perspective — top row is narrower, bottom is wider."""
    # How much to squeeze the top: top width = top_scale * full width
    top_scale    = 0.45
    bottom_scale = 1.00
    scale = top_scale + (bottom_scale - top_scale) * yn
    src_x = 0.5 + (xn - 0.5) / scale
    src_y = yn
    return src_x, src_y


def _warp_wave(xn: np.ndarray, yn: np.ndarray,
               amp_x: float = 0.05, amp_y: float = 0.05,
               freq: float = 3.0):
    """Sinusoidal ripple distortion."""
    src_x = xn + amp_x * np.sin(yn * freq * 2 * np.pi)
    src_y = yn + amp_y * np.sin(xn * freq * 2 * np.pi)
    return src_x, src_y


def _warp_spiral(xn: np.ndarray, yn: np.ndarray, turns: float = 0.9):
    """Logarithmic-spiral / Escher-inspired warp."""
    dx = xn - 0.5
    dy = yn - 0.5
    r     = np.sqrt(dx**2 + dy**2) + 1e-9
    theta = np.arctan2(dy, dx)
    # Rotate proportional to log(r)
    angle = turns * np.log(r + 0.5) * 2 * np.pi
    new_theta = theta + angle
    src_x = 0.5 + r * np.cos(new_theta)
    src_y = 0.5 + r * np.sin(new_theta)
    return src_x, src_y


def _warp_pinch(xn: np.ndarray, yn: np.ndarray):
    """Pinch/squeeze towards the horizontal centre line."""
    dx = xn - 0.5
    dy = yn - 0.5
    r  = np.sqrt(dx**2 + dy**2) + 1e-9
    # Stretch radially outward non-linearly
    new_r = r ** 0.6
    src_x = 0.5 + new_r * dx / r
    src_y = 0.5 + new_r * dy / r
    return src_x, src_y


DISTORTIONS = {
    "polar":       _warp_polar,
    "fisheye":     _warp_fisheye,
    "perspective": _warp_perspective,
    "wave":        _warp_wave,
    "spiral":      _warp_spiral,
    "pinch":       _warp_pinch,
}

DISTORTION_LABELS = {
    "polar":       "Polar / Rund-Verzerrung",
    "fisheye":     "Fischauge / Kugel-Verzerrung",
    "perspective": "Perspektive / Fluchtpunkt",
    "wave":        "Wellen-Verzerrung",
    "spiral":      "Spirale (Escher-Stil)",
    "pinch":       "Quetsch-Verzerrung",
}


# ─────────────────────────────────────────────────────────────────────────────
# CORE: APPLY WARP TO IMAGE
# ─────────────────────────────────────────────────────────────────────────────

def apply_warp(src: np.ndarray, warp_fn) -> np.ndarray:
    """
    Inverse-warp `src` (H×W×C uint8) through `warp_fn`.
    Returns a new uint8 array of the same shape, with out-of-bounds pixels white.
    """
    H, W = src.shape[:2]
    # Build destination pixel grid in normalised [0,1] coords
    ys = np.linspace(0, 1, H)
    xs = np.linspace(0, 1, W)
    xn, yn = np.meshgrid(xs, ys)  # shape (H, W)

    src_x, src_y = warp_fn(xn, yn)

    # Convert back to pixel coordinates
    px = (src_x * (W - 1)).astype(np.float32)
    py = (src_y * (H - 1)).astype(np.float32)

    # Bilinear sampling
    x0 = np.floor(px).astype(np.int32)
    y0 = np.floor(py).astype(np.int32)
    x1 = x0 + 1
    y1 = y0 + 1

    # Clamp
    valid = (x0 >= 0) & (y0 >= 0) & (x1 < W) & (y1 < H)

    x0c = np.clip(x0, 0, W - 1)
    y0c = np.clip(y0, 0, H - 1)
    x1c = np.clip(x1, 0, W - 1)
    y1c = np.clip(y1, 0, H - 1)

    fx = (px - x0).astype(np.float32)[:, :, np.newaxis]
    fy = (py - y0).astype(np.float32)[:, :, np.newaxis]

    c00 = src[y0c, x0c].astype(np.float32)
    c10 = src[y0c, x1c].astype(np.float32)
    c01 = src[y1c, x0c].astype(np.float32)
    c11 = src[y1c, x1c].astype(np.float32)

    result = ((1-fx)*(1-fy)*c00 + fx*(1-fy)*c10 +
              (1-fx)*fy*c01  + fx*fy*c11).astype(np.uint8)

    # White out invalid pixels
    result[~valid] = 255

    return result


# ─────────────────────────────────────────────────────────────────────────────
# GRID DRAWING
# ─────────────────────────────────────────────────────────────────────────────

def draw_regular_grid(img: Image.Image, n_cells: int,
                      colour: str = COL_GRID_SRC,
                      line_width: int = 2,
                      label: bool = True) -> Image.Image:
    """Overlay a uniform n×n grid on img.  Returns a new PIL image."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    W, H = out.size

    for i in range(n_cells + 1):
        x = int(i * W / n_cells)
        y = int(i * H / n_cells)
        draw.line([(x, 0), (x, H)], fill=colour, width=line_width)
        draw.line([(0, y), (W, y)], fill=colour, width=line_width)

    if label:
        # Column letters (A, B, C, …)
        for col in range(n_cells):
            x  = int((col + 0.5) * W / n_cells)
            ch = chr(ord('A') + col % 26)
            _draw_label(draw, ch, x, 6, colour)
        # Row numbers (1, 2, 3, …)
        for row in range(n_cells):
            y  = int((row + 0.5) * H / n_cells)
            _draw_label(draw, str(row + 1), 6, y, colour)

    return out


def _draw_label(draw: ImageDraw.ImageDraw, text: str,
                x: int, y: int, colour: str):
    """Draw a small centred label (no font file needed)."""
    # Use default bitmap font; small but readable
    draw.text((x, y), text, fill=colour, anchor="mm")


def draw_distorted_grid(img: Image.Image, n_cells: int,
                        warp_fn,
                        colour: str = COL_GRID_DIST,
                        line_width: int = 2,
                        label: bool = True,
                        samples: int = 80) -> Image.Image:
    """
    Draw the distorted grid on top of the already-warped image.
    Each grid line is mapped through the *forward* warp: we sample many
    points along each source grid line and draw them in destination space.
    """
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    W, H = out.size

    def src_to_dst(xn_line, yn_line):
        """Forward warp: find where source point (xn, yn) lands in dst."""
        # We have the inverse map; build the forward map via a grid LUT.
        # For display purposes we use numeric differentiation / dense sampling.
        # Simple approach: sample the forward direction by scanning.
        # Since we only need grid lines (not arbitrary points), we use
        # the following approximation: iterate over a dense destination grid,
        # compute the inverse source coordinate, and check proximity.
        # → Too slow for interactive use; instead we directly evaluate the
        #   inverse map on a fine mesh and record where destination cells are.
        pass  # handled below

    # Build a dense forward LUT: src_coords → dst_coords
    # We compute the inverse map on a fine mesh then invert the lookup
    fine = 300
    ys_f = np.linspace(0, 1, fine)
    xs_f = np.linspace(0, 1, fine)
    xn_f, yn_f = np.meshgrid(xs_f, ys_f)  # destination normalised coords

    src_x_f, src_y_f = warp_fn(xn_f, yn_f)  # where each dst pixel comes from

    # For each grid line in source space, draw it in destination space
    def draw_grid_line_h(row_frac):
        """Draw horizontal grid line y=row_frac in source → distorted space."""
        pts_dst = []
        for si in np.linspace(0, 1, samples):
            # find dst pixel closest to source (si, row_frac)
            err = (src_x_f - si)**2 + (src_y_f - row_frac)**2
            idx = np.unravel_index(np.argmin(err), err.shape)
            dst_y = idx[0] / (fine - 1) * H
            dst_x = idx[1] / (fine - 1) * W
            pts_dst.append((dst_x, dst_y))
        for i in range(len(pts_dst) - 1):
            draw.line([pts_dst[i], pts_dst[i+1]], fill=colour, width=line_width)

    def draw_grid_line_v(col_frac):
        pts_dst = []
        for si in np.linspace(0, 1, samples):
            err = (src_x_f - col_frac)**2 + (src_y_f - si)**2
            idx = np.unravel_index(np.argmin(err), err.shape)
            dst_y = idx[0] / (fine - 1) * H
            dst_x = idx[1] / (fine - 1) * W
            pts_dst.append((dst_x, dst_y))
        for i in range(len(pts_dst) - 1):
            draw.line([pts_dst[i], pts_dst[i+1]], fill=colour, width=line_width)

    for i in range(n_cells + 1):
        f = i / n_cells
        draw_grid_line_h(f)
        draw_grid_line_v(f)

    if label:
        # Labels at the centre of each top/left cell edge in dst space
        for col in range(n_cells):
            col_frac = (col + 0.5) / n_cells
            err = (src_x_f - col_frac)**2 + (src_y_f - 0.02)**2
            idx = np.unravel_index(np.argmin(err), err.shape)
            lx = int(idx[1] / (fine-1) * W)
            ly = int(idx[0] / (fine-1) * H)
            ch = chr(ord('A') + col % 26)
            _draw_label(draw, ch, lx, ly, colour)

        for row in range(n_cells):
            row_frac = (row + 0.5) / n_cells
            err = (src_x_f - 0.02)**2 + (src_y_f - row_frac)**2
            idx = np.unravel_index(np.argmin(err), err.shape)
            lx = int(idx[1] / (fine-1) * W)
            ly = int(idx[0] / (fine-1) * H)
            _draw_label(draw, str(row + 1), lx, ly, colour)

    return out


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET COMPOSER
# ─────────────────────────────────────────────────────────────────────────────

def make_worksheet(src_pil: Image.Image,
                   warped_pil: Image.Image,
                   warp_fn,
                   n_cells: int,
                   distortion_name: str,
                   image_name: str,
                   dpi: int = DPI):
    """
    Compose a printable A4-landscape worksheet with:
      - Left:  source image + regular grid
      - Right: warped image + distorted grid
      - Title, instructions, cell reference labels
    Returns a matplotlib Figure.
    """
    label = DISTORTION_LABELS.get(distortion_name, distortion_name)

    src_gridded    = draw_regular_grid(src_pil, n_cells)
    warped_gridded = draw_distorted_grid(warped_pil, n_cells, warp_fn)

    fig = plt.figure(figsize=(16.5, 11.7), dpi=dpi)  # A3-landscape-ish
    fig.patch.set_facecolor(COL_BG)

    # ── Title bar ─────────────────────────────────────────────────────────
    fig.text(0.5, 0.97,
             f"Zeichne nach dem Raster  ·  {label}",
             ha="center", va="top", fontsize=22, fontweight="bold",
             color="#1A1A2E")
    fig.text(0.5, 0.92,
             "Kopiere jedes Kästchen aus dem blauen Raster in das entsprechende "
             "orange Kästchen der verzerrten Seite. Tipp: Fang mit einfachen Kästchen an!",
             ha="center", va="top", fontsize=11, color="#444466",
             style="italic", wrap=True)

    # ── Left panel: regular grid ───────────────────────────────────────────
    ax_src = fig.add_axes([0.03, 0.06, 0.44, 0.82])
    ax_src.imshow(np.array(src_gridded))
    ax_src.set_title("Original – Vorlage",
                     fontsize=15, fontweight="bold", color=COL_GRID_SRC, pad=8)
    ax_src.axis("off")

    # ── Right panel: distorted grid ────────────────────────────────────────
    ax_dst = fig.add_axes([0.53, 0.06, 0.44, 0.82])
    ax_dst.imshow(np.array(warped_gridded))
    ax_dst.set_title("Verzerrt – deine Version",
                     fontsize=15, fontweight="bold", color=COL_GRID_DIST, pad=8)
    ax_dst.axis("off")

    # ── Legend / key ───────────────────────────────────────────────────────
    p1 = mpatches.Patch(color=COL_GRID_SRC,  label="Gleichmäßiges Raster (Vorlage)")
    p2 = mpatches.Patch(color=COL_GRID_DIST, label=f"Verzerrtes Raster ({label})")
    fig.legend(handles=[p1, p2], loc="lower center", ncol=2,
               fontsize=10, framealpha=0.7,
               bbox_to_anchor=(0.5, 0.01))

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# BLANK WORKSHEET (empty distorted grid for the kid to draw into)
# ─────────────────────────────────────────────────────────────────────────────

def make_blank_worksheet(src_pil: Image.Image,
                         warp_fn,
                         n_cells: int,
                         distortion_name: str,
                         dpi: int = DPI):
    """
    Worksheet variant:
      - Left:  source image + regular grid (reference)
      - Right: BLANK white image + distorted grid (kid draws here)
    """
    label = DISTORTION_LABELS.get(distortion_name, distortion_name)
    src_gridded = draw_regular_grid(src_pil, n_cells)

    # Blank white image with distorted grid
    blank_pil   = Image.new("RGB", src_pil.size, "#FFFEF6")
    blank_grid  = draw_distorted_grid(blank_pil, n_cells, warp_fn,
                                      line_width=3)

    fig = plt.figure(figsize=(16.5, 11.7), dpi=dpi)
    fig.patch.set_facecolor(COL_BG)

    fig.text(0.5, 0.97,
             f"Zeichne selbst!  ·  {label}",
             ha="center", va="top", fontsize=22, fontweight="bold",
             color="#1A1A2E")
    fig.text(0.5, 0.92,
             "Schau dir das Bild links an und übertrage jedes Kästchen "
             "in das entsprechende verzerrte Kästchen rechts.",
             ha="center", va="top", fontsize=11, color="#444466",
             style="italic")

    ax_src = fig.add_axes([0.03, 0.06, 0.44, 0.82])
    ax_src.imshow(np.array(src_gridded))
    ax_src.set_title("Vorlage – was du abzeichnen sollst",
                     fontsize=14, fontweight="bold", color=COL_GRID_SRC, pad=8)
    ax_src.axis("off")

    ax_dst = fig.add_axes([0.53, 0.06, 0.44, 0.82])
    ax_dst.imshow(np.array(blank_grid))
    ax_dst.set_title("Hier zeichnen ✏️",
                     fontsize=14, fontweight="bold", color=COL_GRID_DIST, pad=8)
    ax_dst.axis("off")

    p1 = mpatches.Patch(color=COL_GRID_SRC,  label="Gleichmäßiges Raster (Vorlage)")
    p2 = mpatches.Patch(color=COL_GRID_DIST, label=f"Verzerrtes Raster ({label})")
    fig.legend(handles=[p1, p2], loc="lower center", ncol=2,
               fontsize=10, framealpha=0.7,
               bbox_to_anchor=(0.5, 0.01))

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate Escher-style grid drawing worksheets for kids.")
    parser.add_argument("--builtin",
                        choices=list(BUILTIN_IMAGES.keys()),
                        default="house",
                        help="Built-in line-art image to use (default: house)")
    parser.add_argument("--image",
                        type=str,
                        default=None,
                        help="Path to a custom image file (overrides --builtin)")
    parser.add_argument("--distortion",
                        choices=list(DISTORTIONS.keys()) + ["all"],
                        default="all",
                        help="Distortion type to apply (default: all)")
    parser.add_argument("--grid",
                        type=int,
                        default=8,
                        help="Number of grid cells per side (default: 8)")
    parser.add_argument("--no-blank",
                        action="store_true",
                        help="Skip generating the blank drawing worksheet")
    parser.add_argument("--size",
                        type=int,
                        default=IMG_SIZE,
                        help=f"Image render size in pixels (default: {IMG_SIZE})")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load / create source image ──────────────────────────────────────────
    if args.image:
        src_pil = Image.open(args.image).convert("RGB")
        src_pil = src_pil.resize((args.size, args.size), Image.LANCZOS)
        image_name = Path(args.image).stem
    else:
        src_pil    = make_builtin_image(args.builtin, args.size)
        image_name = args.builtin

    src_np = np.array(src_pil)

    # ── Determine which distortions to run ─────────────────────────────────
    if args.distortion == "all":
        dist_list = list(DISTORTIONS.keys())
    else:
        dist_list = [args.distortion]

    print(f"\n{'='*60}")
    print(f"  Escher Grid Drawing Generator")
    print(f"  Image : {image_name}  |  Grid: {args.grid}×{args.grid}")
    print(f"  Output: {OUTPUT_DIR.resolve()}")
    print(f"{'='*60}\n")

    for dist_name in dist_list:
        warp_fn = DISTORTIONS[dist_name]
        label   = DISTORTION_LABELS[dist_name]
        print(f"  [{dist_name}]  {label} …", end="", flush=True)

        # Warp the image
        warped_np  = apply_warp(src_np, warp_fn)
        warped_pil = Image.fromarray(warped_np)

        stem = f"{image_name}_{dist_name}"

        # ── A) Reference worksheet (image shown on both sides) ──────────────
        fig = make_worksheet(src_pil, warped_pil, warp_fn,
                             args.grid, dist_name, image_name)
        for ext in ("png", "pdf"):
            path = OUTPUT_DIR / f"{stem}.{ext}"
            fig.savefig(path, dpi=DPI, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
        plt.close(fig)

        # ── B) Blank worksheet (kid draws here) ────────────────────────────
        if not args.no_blank:
            fig_blank = make_blank_worksheet(src_pil, warp_fn,
                                             args.grid, dist_name)
            for ext in ("png", "pdf"):
                path = OUTPUT_DIR / f"{stem}_blank.{ext}"
                fig_blank.savefig(path, dpi=DPI, bbox_inches="tight",
                                  facecolor=fig_blank.get_facecolor())
            plt.close(fig_blank)

        print("  ✓")

    print(f"\n  Done! {len(dist_list) * (1 + (0 if args.no_blank else 1))} "
          f"worksheets saved to {OUTPUT_DIR.resolve()}\n")


if __name__ == "__main__":
    main()
