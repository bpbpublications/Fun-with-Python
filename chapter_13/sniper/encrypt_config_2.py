import click
import json
from cryptography.fernet import Fernet


def main():
    cc_name = click.prompt("Enter a credit card name", type=str)
    if not cc_name:
        return
    cc_nubmer_default = int("1" * 16)
    cc_number = click.prompt(
        "Enter a credit card number", type=click.IntRange(cc_nubmer_default), default=cc_nubmer_default
    )
    if not cc_number:
        return
    cc_exp_month = click.prompt("Enter a credit card expiry month", type=click.IntRange(1, 12), default=1)
    if not cc_exp_month:
        return
    cc_exp_year = click.prompt("Enter a credit card expiry month", type=click.IntRange(2024, 2050), default=2025)
    if not cc_exp_month:
        return

    data = json.dumps({"name": cc_name, "numbert": cc_number, "month": cc_exp_month, "year": cc_exp_year}).encode(
        "utf-8"
    )

    with open("key", "rb") as f:
        key = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open("cc.data", "wb") as f:
        f.write(encrypted)


if __name__ == "__main__":
    main()
