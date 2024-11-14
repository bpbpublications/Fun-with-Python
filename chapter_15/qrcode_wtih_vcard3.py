import pyqrcode
import yaml
from PIL import Image
from datetime import datetime


def read_config():
    with open("contact.yaml", "r") as file:
        return yaml.safe_load(file)


def create_vcard(data):
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


def generate_code(data, name, surname):
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
    final_qr_code = f"/tmp/{name}_{surname}.png"
    print(f"Saving QR code: {final_qr_code}")
    im.save(final_qr_code, "PNG")


if __name__ == "__main__":
    vcards = read_config()["contact"]
    for item in vcards:
        print(f"Creating vCards for {item['name']} {item['surname']}")
        vcard = create_vcard(item)
        generate_code(vcard, item["name"], item["surname"])
