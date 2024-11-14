from PIL import Image
from pyzbar.pyzbar import decode

result = decode(Image.open("/tmp/John_Smith.png"))
print("decodeing result:")
print(result[0].data)
