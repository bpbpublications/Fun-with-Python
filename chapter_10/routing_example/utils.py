import random


def get_client_ip(client_ip):
    return f"10.65.0.{20+client_ip}"


def get_client_mac_address(client_ip):
    return f"01.00.0f.ff.af.{20+client_ip}"


def random_mac_address():
    mac_addresss = "01:00:00"
    choices = "0123456789abcdef"
    for _ in range(3):
        mac_addresss += ":{}{}".format(*random.choices(choices, k=2))
    return mac_addresss


def random_client_ip():
    ip_addresss = ""
    for _ in range(4):
        ip_addresss += f"{(random.randint(100, 254))}."
    return ip_addresss[:-1]
