import xml.etree.ElementTree as ET
import re

# Read the SVG
tree = ET.parse('italy.svg')
root = tree.getroot()

# The namespace is usually something like {http://www.w3.org/2000/svg}
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Combine all paths into one
combined_path = []
for path in root.findall('.//svg:path', ns):
    d = path.attrib.get('d', '')
    if d:
        combined_path.append(d)

full_d = " ".join(combined_path)

# Extract all coordinates to find bounding box
coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', full_d)
coords = [float(c) for c in coords]
# Note: SVG paths have commands (M, L, C, etc.) and coords.
# A simple way to scale a path is to parse commands, scale numbers.

def scale_path(path_str, target_size=20, offset=2):
    # Tokenize path
    tokens = re.findall(r'[a-zA-Z]|[-+]?\d*\.\d+|[-+]?\d+', path_str)
    
    # Find bounding box
    x_coords = []
    y_coords = []
    i = 0
    while i < len(tokens):
        if re.match(r'[-+]?\d*\.\d+|[-+]?\d+', tokens[i]):
            x_coords.append(float(tokens[i]))
            if i + 1 < len(tokens) and re.match(r'[-+]?\d*\.\d+|[-+]?\d+', tokens[i+1]):
                y_coords.append(float(tokens[i+1]))
                i += 1
        i += 1
        
    if not x_coords: return path_str
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    width = max_x - min_x
    height = max_y - min_y
    scale = target_size / max(width, height)
    
    dx = offset - min_x * scale + (target_size - width * scale) / 2
    dy = offset - min_y * scale + (target_size - height * scale) / 2
    
    # Rebuild path
    new_path = []
    i = 0
    is_x = True
    while i < len(tokens):
        if re.match(r'[-+]?\d*\.\d+|[-+]?\d+', tokens[i]):
            val = float(tokens[i])
            if is_x:
                val = val * scale + dx
            else:
                val = val * scale + dy
            new_path.append(f"{val:.2f}")
            # toggle for next coordinate
            # Note: commands like 'H' and 'V' take only one coordinate
            cmd = "L"
            # we need to accurately know if it's X or Y, which requires a full parser.
            # since this is hard, let's just use an SVG transform instead!
        else:
            new_path.append(tokens[i])
            cmd = tokens[i].upper()
            if cmd in ('H', 'V'):
                # H is x, V is y. We won't handle them perfectly here but they are rare in geodata
                pass
        # simpler to just use <g transform="..."> in the SVG
        i += 1
    # return " ".join(new_path)
    return ""

# Wait, instead of parsing paths, we can just output the SVG with the original viewBox and let it scale automatically!
# Original viewBox of amCharts italy is "0 0 800 800" roughly. Let's extract the viewBox from italy.svg.
viewbox = root.attrib.get('viewBox', '0 0 1000 1000')

# Create the final SVG string
final_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="{viewbox}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <g transform="scale(1) translate(0, 0)">
        <path d="{full_d}"></path>
    </g>
</svg>'''

# To match stroke-width="2" on a 24x24, if viewBox is say 1000x1000, stroke-width needs to be 1000/24 * 2 = 83.
vb_parts = [float(x) for x in viewbox.split()]
vb_width = vb_parts[2] if len(vb_parts) >= 3 else 1000
stroke_width = (vb_width / 24) * 2

final_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="{viewbox}" fill="none" stroke="currentColor" stroke-width="{stroke_width:.1f}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{full_d}"></path>
</svg>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the previous map icon with the new one
html = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4l4-2 3 1.*?></svg>', final_svg, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Replaced successfully!")
