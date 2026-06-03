import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add reveal class to main wrappers (like section divs or columns)
html = re.sub(r'(class="grid grid-cols-1 md:grid-cols-3)', r'class="reveal grid grid-cols-1 md:grid-cols-3', html)
html = re.sub(r'(<div>\s*<div class="flex items-center gap-4 mb-8">)', r'<div class="reveal">\n                        <div class="flex items-center gap-4 mb-8">', html)
html = re.sub(r'(<div class="border-2 border-brand-red)', r'<div class="reveal border-2 border-brand-red', html)
html = re.sub(r'(<div class="p-8">)', r'<div class="reveal p-8">', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
