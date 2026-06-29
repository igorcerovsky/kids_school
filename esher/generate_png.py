import matplotlib
matplotlib.use("Agg")
from generate_3b1b_grid import draw_3b1b_escher_grid
draw_3b1b_escher_grid("3b1b_test", recursions=2)
import xml.etree.ElementTree as ET
from xml.dom import minidom
# Also let's print the value of wx_bl and wy_bl
