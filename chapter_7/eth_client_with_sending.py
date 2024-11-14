import click
import configparser
from decimal import Decimal
from web3 import Web3


config = configparser.ConfigParser()
config.sections()
config.read("config.ini")

eth_server = config.get("network", "server")
main_wallet = config.get("wallet", "main")
trade_wallet = config.get("wallet", "trade")
main_private_key = config.get("wallet", "main_key")

w3 = Web3(Web3.HTTPProvider(eth_server))
print("Are we connected", w3.is_connected())


def make_transfer(account_src, account_dst, private_key, amount) -> str:
    # we need nonce for transaction
    nonce = w3.eth.get_transaction_count(account_src)
    # transaciton data
    tx = {
        "nonce": nonce,
        "to": account_dst,
        "value": w3.to_wei(Decimal(amount), "ether"),
        "gas": 21000,
        "maxFeePerGas": 20000000000,
        "maxPriorityFeePerGas": 1000000000,
        "chainId": w3.eth.chain_id,
    }
    signed_tx = w3.eth.account.sign_transaction(tx, main_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)


def check_ballance(wallet_address):
    balance = w3.eth.get_balance(wallet_address)
    human_blance = w3.from_wei(balance, "ether")
    print(f"balance: {human_blance:.2f}")
    return human_blance


@click.command()
@click.option("--amount", help="Amount of ETH to send", required=False, type=float)
@click.option("--send", help="Send coins to destination wallet", required=False, default=False, is_flag=True)
@click.option("--balance", help="Show wallets balance", required=False, default=False, is_flag=True)
def main(balance, send, amount):
    if balance:
        check_ballance(main_wallet)
        check_ballance(trade_wallet)
    if send:
        assert amount, "Amount to send is required"
        result = make_transfer(main_wallet, trade_wallet, main_private_key, amount)
        print(f"Sending transaction id: {result}")


if __name__ == "__main__":
    main()
