import xml.etree.ElementTree as ET
tree = ET.parse('output_escher/3b1b_original_escher_grid.svg')
root = tree.getroot()
ns = {'svg': 'http://www.w3.org/2000/svg'}
count = 0
for path in root.findall('.//svg:path', ns):
    style = path.get('style', '')
    if '#27ae60' in style:
        count += 1
print(f"Found {count} green paths")
