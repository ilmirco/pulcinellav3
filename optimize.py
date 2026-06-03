from PIL import Image
import re

# 1. Image Conversion
img = Image.open('pizza-bg.png')
img.save('pizza-bg.webp', 'WEBP', quality=80)
img.thumbnail((800, 800))
img.save('pizza-bg-mobile.webp', 'WEBP', quality=80)
img.save('pizza-bg-mobile.jpg', 'JPEG', quality=80)
print('Images converted.')

# 2. SVG Minification
with open('logo.svg', 'r', encoding='utf-8') as f:
    svg_data = f.read()

# Remove comments
svg_data = re.sub(r'<!--.*?-->', '', svg_data, flags=re.DOTALL)
# Remove extra whitespace
svg_data = re.sub(r'>\s+<', '><', svg_data)
svg_data = re.sub(r'\s+', ' ', svg_data)

with open('logo.svg', 'w', encoding='utf-8') as f:
    f.write(svg_data)
print('SVG minified.')
