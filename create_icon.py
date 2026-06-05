from PIL import Image, ImageDraw, ImageFont
size = 180
img = Image.new('RGB', (size, size), (255, 255, 255))
draw = ImageDraw.Draw(img)
ring_width = 10
bounding_box = [15, 15, size-15, size-15]
draw.arc(bounding_box, -90, 90, fill=(204, 21, 21), width=ring_width)
draw.arc(bounding_box, 90, 270, fill=(26, 107, 42), width=ring_width)
try:
    font = ImageFont.truetype('georgia.ttf', 100)
except:
    try:
        font = ImageFont.truetype('arial.ttf', 100)
    except:
        font = ImageFont.load_default()

try:
    draw.text((size/2, size/2 - 5), 'P', fill=(17, 17, 17), font=font, anchor='mm')
except TypeError:
    bbox = draw.textbbox((0,0), 'P', font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((size/2 - w/2, size/2 - h/2 - 15), 'P', fill=(17, 17, 17), font=font)

img.save('apple-touch-icon.png')
