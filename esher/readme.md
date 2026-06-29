# Escher's Print Gallery: Droste Effect Generator

This project generates the mathematically exact conformal mapping behind M.C. Escher's famous lithograph *Print Gallery*, leveraging the geometry analyzed by Hendrik Lenstra and visualized by 3Blue1Brown.

It uses complex mapping to transform a Cartesian grid and an underlying image into the continuous, self-similar logarithmic spiral known as the **Droste effect**.

## The Mathematics

The core transformation maps the complex plane $Z$ (the unwarped grid) to the complex plane $W$ (the spiral) using the conformal map:

$$ W = Z^\beta $$

Where $\beta$ is a complex constant designed to perfectly map a geometric scaling of the image to a full $2\pi$ rotation. For a base scale factor of `16.0` (meaning the grid repeats every factor of 16), $\beta$ is defined as:

$$ \beta = \frac{2\pi i}{\ln(16) + 2\pi i} $$

### Key Features
- **Perfect Continuity:** By meticulously tracking the branch cuts of the complex logarithm and unwrapping the angles of the grid lines, the generated spiral is perfectly continuous without the "overlapping" artifacts common in naive implementations.
- **Geometric Grid Scaling:** The underlying grid density recursively scales by a factor of exactly `2.0` towards the center, accurately reproducing the grid geometry from the original 3b1b animation.
- **Conformal Image Warping:** Any input image can be mapped onto the spiral using inverse bilinear sampling. 

## Scripts and Usage

### 1. The Worksheet Generator (`generate_escher.py`)
This is the primary script to generate an educational worksheet. It outputs a side-by-side comparison of the unwarped mathematically scaled grid and the final Escher-warped spiral, complete with customizable axis labels and tick marks.

**Usage:**
```bash
python esher/generate_escher.py --image esher/img/motyl.jpg --preset tight
```
- `--image`: The path to the texture you want to map.
- `--preset`: Automatically configures the grid size and scaling ratio (`tight` uses a factor of 16, `esher` uses the original 256).

### 2. The Pristine 3b1b Renderer (`generate_3b1b_grid.py`)
This script strips away the worksheet formatting (labels, ticks, titles) to output the pure, mathematical vector rendering of the grid and image mapping, matching the exact aesthetic of the 3Blue1Brown video. 

**Usage:**
```bash
python esher/generate_3b1b_grid.py --ratio 16.0 --turns 1.0 --recursions 6 --image esher/img/pi.png --out my_render
```
- `--ratio`: The geometric factor at which the image tiles (default: `16.0`).
- `--turns`: The number of spiral twists per scaling (default: `1.0`).
- `--recursions`: How many factors of 2 the grid expands outwards.

## Understanding the "Droste" Image Tiling
If you input a standard photograph (like `motyl.jpg`), you will notice a square "tear" spiraling through the image. **This is mathematically correct.**

The conformal mapping connects the outer boundary of the image directly to its inner center (scaled down by the `ratio`). Because the outer border of a standard photo does not match its center, a severe discontinuity appears. 

To achieve a flawless, seamless spiral (like Escher's original painting or the `pi.png` animation), the input image must be **"Droste-Seamless"**—specifically edited so that its central pixels seamlessly transition into its outer border. When mapped, the seamless square image will perfectly swallow itself into infinity.
