"""
Script per creare l'icona di DocConverter
"""
from PIL import Image, ImageDraw, ImageFont

# Crea immagine 256x256 (per .ico)
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Sfondo gradiente blu/verde
for y in range(size):
    color = (20, 160 + int(y * 0.2), 133 - int(y * 0.1), 255)
    draw.rectangle([(0, y), (size, y+1)], fill=color)

# Arrotonda gli angoli
from PIL import ImageDraw
mask = Image.new('L', (size, size), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=30, fill=255)
img.putalpha(mask)

# Aggiungi icona documento (rettangolo bianco)
doc_color = (255, 255, 255, 255)
doc_x = size // 4
doc_y = size // 6
doc_w = size // 2
doc_h = int(size * 0.65)

# Documento con piega
draw.rectangle([(doc_x, doc_y), (doc_x + doc_w, doc_y + doc_h)], fill=doc_color)
draw.polygon([(doc_x + doc_w - 30, doc_y), (doc_x + doc_w, doc_y + 30), (doc_x + doc_w, doc_y)], fill=(200, 200, 200, 255))

# Aggiungi freccia PDF (simbolo →)
arrow_color = (255, 100, 100, 255)
arrow_size = 40
arrow_x = size // 2 - arrow_size // 2
arrow_y = size - 70
draw.text((arrow_x, arrow_y), "→", fill=arrow_color, font=None)

# Aggiungi testo "PDF"
text_color = (50, 50, 50, 255)
text_y = size - 50
draw.text((size//2 - 25, text_y), "PDF", fill=text_color, font=None)

# Salva come PNG
img.save('assets/icon.png')
print("✅ Icon PNG creato: assets/icon.png")

# Salva come ICO (per Windows)
img.save('assets/icon.ico', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("✅ Icon ICO creato: assets/icon.ico")

print("\n✅ Icone create con successo!")
