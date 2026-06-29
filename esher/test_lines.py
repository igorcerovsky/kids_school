def get_nested_square_grid_lines(grid_size, height, scale_factor):
    lines = []
    H = height
    h = height / scale_factor
    for i in range(grid_size + 1):
        pos = -H + (2 * H * i) / grid_size
        eps = 1e-9
        if -h + eps < pos < h - eps:
            lines.append((pos, H, pos, h))
            lines.append((pos, -h, pos, -H))
        else:
            lines.append((pos, H, pos, -H))
        if -h + eps < pos < h - eps:
            lines.append((H, pos, h, pos))
            lines.append((-h, pos, -H, pos))
        else:
            lines.append((H, pos, -H, pos))
    return lines

base_lines = get_nested_square_grid_lines(grid_size=8, height=1.0, scale_factor=2.0)
H_val = 1.0
count = 0
for (x0, y0, x1, y1) in base_lines:
    is_perimeter = ((abs(abs(x0) - H_val) < 1e-9 and abs(abs(x1) - H_val) < 1e-9) or 
                    (abs(abs(y0) - H_val) < 1e-9 and abs(abs(y1) - H_val) < 1e-9))
    if is_perimeter:
        count += 1
        print(f"Perimeter line: ({x0}, {y0}) to ({x1}, {y1})")
print(f"Total perimeter lines: {count}")
