import urllib.request
import xml.etree.ElementTree as ET
import re

req = urllib.request.Request(
    'https://upload.wikimedia.org/wikipedia/commons/e/e0/Italy_silhouette.svg',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
try:
    with urllib.request.urlopen(req) as response:
        svg_content = response.read().decode('utf-8')
    with open('italy.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
except Exception as e:
    print("Download failed:", e)
    exit(1)

# Read the SVG
tree = ET.parse('italy.svg')
root = tree.getroot()

# The namespace
ns = {'svg': 'http://www.w3.org/2000/svg'}

combined_path = []
# look for paths anywhere
for path in root.iter('{http://www.w3.org/2000/svg}path'):
    d = path.attrib.get('d', '')
    if d:
        combined_path.append(d)

full_d = " ".join(combined_path)

viewbox = root.attrib.get('viewBox', '0 0 1000 1000')

vb_parts = [float(x) for x in viewbox.split()]
vb_width = vb_parts[2] if len(vb_parts) >= 3 else 1000
stroke_width = (vb_width / 24) * 2

final_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="{viewbox}" fill="none" stroke="currentColor" stroke-width="{stroke_width:.1f}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{full_d}"></path>
</svg>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4l4-2 3 1.*?></svg>', final_svg, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Replaced successfully with Wikimedia SVG!")
