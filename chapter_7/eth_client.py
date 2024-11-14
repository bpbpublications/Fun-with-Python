import configparser
from web3 import Web3


config = configparser.ConfigParser()
config.sections()
config.read("config.ini")

eth_server = config.get("network", "server")
main_wallet = config.get("wallet", "main")
trade_wallet = config.get("wallet", "trade")

w3 = Web3(Web3.HTTPProvider(eth_server))
print("Are we connected", w3.is_connected())


def check_ballance(wallet_address):
    balance = w3.eth.get_balance(wallet_address)
    human_blance = w3.from_wei(balance, "ether")
    print(f"balance: {human_blance:.2f}")


if __name__ == "__main__":
    check_ballance(main_wallet)
    check_ballance(trade_wallet)
