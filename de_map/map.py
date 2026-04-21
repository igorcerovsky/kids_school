import xml.etree.ElementTree as ET

from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale, translate

from svgpathtools import parse_path

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg


# =========================
# SETTINGS
# =========================

SVG_FILE = "de_map/Map_Germany_Länder-de.svg"
OUTPUT_FILE = "de_map/Bundeslaender_Puzzle_A4.pdf"

SHOW_NAMES = True

A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297

MARGIN_MM = 10

MM_TO_PT = 2.83465

USABLE_WIDTH = A4_WIDTH_MM - 2 * MARGIN_MM
USABLE_HEIGHT = A4_HEIGHT_MM - 2 * MARGIN_MM

PACK_GAP = 5

CURVE_STEPS = 30


# =========================
# SAMPLE SVG PATH
# =========================

def sample_svg_path(d):

    path = parse_path(d)

    pts = []

    for segment in path:

        for i in range(CURVE_STEPS):

            t = i / CURVE_STEPS

            p = segment.point(t)

            pts.append((p.real, p.imag))

    return pts


# =========================
# LOAD GROUPED POLYGONS
# =========================

def load_bundeslaender():

    tree = ET.parse(SVG_FILE)
    root = tree.getroot()

    ns = {"svg": "http://www.w3.org/2000/svg"}

    bundeslaender = []

    for g in root.findall(".//svg:g", ns):

        name = g.attrib.get("id")

        if not name:
            continue

        paths = g.findall(".//svg:path", ns)

        polygons = []

        for p in paths:

            d = p.attrib.get("d")

            if not d:
                continue

            pts = sample_svg_path(d)

            if len(pts) < 3:
                continue

            poly = Polygon(pts)

            if not poly.is_valid:
                continue

            polygons.append(poly)

        if polygons:

            if len(polygons) == 1:

                bundeslaender.append(
                    (name, polygons[0])
                )

            else:

                bundeslaender.append(
                    (name, MultiPolygon(polygons))
                )

    print("Bundesländer detected:", len(bundeslaender))

    return bundeslaender


# =========================
# SORT
# =========================

def sort_by_size(bundeslaender):

    return sorted(
        bundeslaender,
        key=lambda x: x[1].area,
        reverse=True
    )


# =========================
# SCALE
# =========================

def scale_to_a4(bundeslaender):

    largest = max(
        bundeslaender,
        key=lambda x: x[1].area
    )[1]

    minx, miny, maxx, maxy = largest.bounds

    width = maxx - minx
    height = maxy - miny

    scale_x = USABLE_WIDTH / width
    scale_y = USABLE_HEIGHT / height

    scale_factor = min(scale_x, scale_y)

    scaled = []

    for name, poly in bundeslaender:

        new_poly = scale(
            poly,
            xfact=scale_factor,
            yfact=scale_factor,
            origin=(0, 0)
        )

        scaled.append((name, new_poly))

    return scaled


# =========================
# PACK
# =========================

def pack_polygons(bundeslaender):

    pages = []

    current = []

    x_cursor = 0
    y_cursor = 0
    row_height = 0

    for name, poly in bundeslaender:

        minx, miny, maxx, maxy = poly.bounds

        w = maxx - minx
        h = maxy - miny

        if x_cursor + w > USABLE_WIDTH:

            x_cursor = 0
            y_cursor += row_height + PACK_GAP
            row_height = 0

        if y_cursor + h > USABLE_HEIGHT:

            pages.append(current)

            current = []

            x_cursor = 0
            y_cursor = 0
            row_height = 0

        moved = translate(
            poly,
            xoff=x_cursor - minx,
            yoff=y_cursor - miny
        )

        current.append((name, moved))

        x_cursor += w + PACK_GAP

        row_height = max(row_height, h)

    if current:
        pages.append(current)

    print("Pages created:", len(pages))

    return pages


# =========================
# REFERENCE PAGE
# =========================

def draw_reference_svg(c):

    drawing = svg2rlg(SVG_FILE)

    width = drawing.width
    height = drawing.height

    scale_x = (USABLE_WIDTH * MM_TO_PT) / width
    scale_y = (USABLE_HEIGHT * MM_TO_PT) / height

    scale_factor = min(scale_x, scale_y)

    drawing.scale(scale_factor, scale_factor)

    c.saveState()

    c.translate(
        MARGIN_MM * MM_TO_PT,
        MARGIN_MM * MM_TO_PT
    )

    renderPDF.draw(drawing, c, 0, 0)

    c.restoreState()

    c.showPage()


# =========================
# DRAW PAGE
# =========================

def draw_page(c, polygons):

    c.saveState()

    c.translate(
        MARGIN_MM * MM_TO_PT,
        MARGIN_MM * MM_TO_PT
    )

    for name, poly in polygons:

        if isinstance(poly, MultiPolygon):

            plist = poly.geoms

        else:

            plist = [poly]

        for p in plist:

            path = c.beginPath()

            coords = list(p.exterior.coords)

            path.moveTo(
                coords[0][0] * MM_TO_PT,
                coords[0][1] * MM_TO_PT
            )

            for x, y in coords[1:]:

                path.lineTo(
                    x * MM_TO_PT,
                    y * MM_TO_PT
                )

            path.close()

            c.drawPath(path)

        if SHOW_NAMES:

            cx = poly.centroid.x * MM_TO_PT
            cy = poly.centroid.y * MM_TO_PT

            c.setFont("Helvetica", 8)

            c.drawString(cx, cy, name)

    c.restoreState()

    c.showPage()


# =========================
# MAIN
# =========================

def main():

    print("Loading Bundesländer...")
    bundeslaender = load_bundeslaender()

    print("Sorting...")
    bundeslaender = sort_by_size(bundeslaender)

    print("Scaling...")
    bundeslaender = scale_to_a4(bundeslaender)

    print("Packing...")
    pages = pack_polygons(bundeslaender)

    print("Generating PDF...")

    c = canvas.Canvas(
        OUTPUT_FILE,
        pagesize=(
            A4_WIDTH_MM * MM_TO_PT,
            A4_HEIGHT_MM * MM_TO_PT
        )
    )

    draw_reference_svg(c)

    for page in pages:
        draw_page(c, page)

    c.save()

    print("Done!")
    print("Saved as:", OUTPUT_FILE)


if __name__ == "__main__":
    main()