import pyqrcode
import yaml
from PIL import Image
from datetime import datetime


def read_config():
    with open("contact.yaml", "r") as file:
        return yaml.safe_load(file)


def create_vcard():
    data = read_config()["contact"][0]
    now_with_zulu = datetime.utcnow().isoformat()[:-3] + "Z"

    vcard_data = f"""BEGIN:VCARD
    VERSION:4.0
    FN;CHARSET=UTF-8:{data['name']} {data['surname']}
    N;CHARSET=UTF-8:{data['surname']};{data['name']};;;
    """
    if data.get("gender", "").lower() == "male":
        vcard_data += "GENDER:M\n\r"
    if data.get("gender", "").lower() == "female":
        vcard_data += "GENDER:F\n\r"

    birth_date = data["birthday"]
    vcard_data += f"BDAY:{birth_date.strftime('%Y%m%d')}\n\r"
    home_address = data["address"]["home"]
    vcard_data += f"""ADR;CHARSET=UTF-8;TYPE=HOME:;;{home_address['street']};{home_address['city']};;{home_address['code']};{home_address['country']}
    TITLE;CHARSET=UTF-8:{data['org']['title']}
    ROLE;CHARSET=UTF-8:{data['org']['role']}
    ORG;CHARSET=UTF-8:{data['org']['name']}
    REV:{now_with_zulu}
    END:VCARD"""
    return vcard_data


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
    vcard = create_vcard()
    print(vcard)
    generate_code(vcard)
