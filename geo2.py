import urllib.request
import json
import re
import math

req = urllib.request.Request('https://raw.githubusercontent.com/johan/world.geo.json/master/countries/ITA.geo.json')
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print("Download failed:", e)
    exit(1)

polygons = []
if data['features'][0]['geometry']['type'] == 'Polygon':
    polygons = [data['features'][0]['geometry']['coordinates']]
elif data['features'][0]['geometry']['type'] == 'MultiPolygon':
    polygons = data['features'][0]['geometry']['coordinates']

# Collect all points
all_x = []
all_y = []

# Italy mean latitude is ~42 degrees
cos_lat = math.cos(math.radians(42.0))

for poly in polygons:
    for ring in poly:
        for pt in ring:
            # apply simple projection correction
            all_x.append(pt[0] * cos_lat)
            all_y.append(-pt[1])

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

width = max_x - min_x
height = max_y - min_y

# Scale to fit in 22x22 box (leaving 1px padding for 24x24) to make it larger
TARGET_SIZE = 22
OFFSET = 1
scale = TARGET_SIZE / max(width, height)
dx = OFFSET - min_x * scale + (TARGET_SIZE - width * scale) / 2
dy = OFFSET - min_y * scale + (TARGET_SIZE - height * scale) / 2

# Build the SVG path
path_commands = []
for poly in polygons:
    for ring in poly:
        for i, pt in enumerate(ring):
            x = pt[0] * cos_lat * scale + dx
            y = -pt[1] * scale + dy
            if i == 0:
                path_commands.append(f"M {x:.2f} {y:.2f}")
            else:
                path_commands.append(f"L {x:.2f} {y:.2f}")
        path_commands.append("Z")

full_d = " ".join(path_commands)

final_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
    <path d="{full_d}"></path>
</svg>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the previous GeoJSON SVG
html = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">.*?<\/svg>', final_svg, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("GeoJSON injected successfully with projection correction!")
