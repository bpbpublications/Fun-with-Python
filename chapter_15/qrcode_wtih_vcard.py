import pyqrcode
from PIL import Image

vcard_data = """BEGIN:VCARD
VERSION:4.0
FN:John Smith
N:John;Smith;;;ing. jr,M.Sc.
BDAY:--0102
GENDER:M
EMAIL;TYPE=work:joshn.smith@fooooo.com
END:VCARD"""


def generate_code(data):
    url = pyqrcode.QRCode(data, error="H")
    url.png("test.png", scale=10)
    im = Image.open("test.png")
    im = im.convert("RGBA")

    logo = Image.open("python-logo.png")
    box = (145, 145, 235, 235)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    x = int(im.size[0] / 2) - int(region.size[0] / 2)
    y = int(im.size[1] / 2) - int(region.size[1] / 2)
    im.paste(region, (x, y))
    im.show()


if __name__ == "__main__":
    generate_code(vcard_data)
