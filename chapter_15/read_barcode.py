import cv2
import numpy as np
from cairosvg import svg2png
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol

OUTPUT_FILE = "/tmp/cv.png"


with open("/tmp/somefile.svg", "r") as f:
    png = svg2png(file_obj=f)

pil_img = Image.open(BytesIO(png)).convert("RGBA")
pil_img.save("/tmp/tmp_barcode.png")

cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
cv2.imwrite(OUTPUT_FILE, cv_img)

img = cv2.imread(OUTPUT_FILE)
detectedBarcodes = decode(img, symbols=[ZBarSymbol.EAN13])
barcode = detectedBarcodes[0]
# result
print(barcode)
print(f"Scanned code: {barcode.data}")
