import urllib.request
import json
import re

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

# Collect all points to find bounding box
all_x = []
all_y = []
for poly in polygons:
    for ring in poly:
        for pt in ring:
            # Note: GeoJSON is [lon, lat]
            # Latitude is inverted in SVG (higher lat = lower Y)
            all_x.append(pt[0])
            all_y.append(-pt[1])

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

width = max_x - min_x
height = max_y - min_y

# Scale to fit in 20x20 box (leaving 2px padding for 24x24)
scale = 20 / max(width, height)
dx = 2 - min_x * scale + (20 - width * scale) / 2
dy = 2 - min_y * scale + (20 - height * scale) / 2

# Build the SVG path
path_commands = []
for poly in polygons:
    for ring in poly:
        for i, pt in enumerate(ring):
            x = pt[0] * scale + dx
            y = -pt[1] * scale + dy
            if i == 0:
                path_commands.append(f"M {x:.2f} {y:.2f}")
            else:
                path_commands.append(f"L {x:.2f} {y:.2f}")
        path_commands.append("Z")

full_d = " ".join(path_commands)

final_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
    <path d="{full_d}"></path>
</svg>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4l4-2 3 1.*?></svg>', final_svg, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("GeoJSON injected successfully!")
