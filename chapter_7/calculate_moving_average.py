import click
import numpy as np
from db import DB
from decimal import Decimal
from eth_client_with_sending import make_transfer, main_wallet, trade_wallet, main_private_key, check_ballance


class AnalyzeRates:
    def __init__(self, currency):
        self.currency = currency
        self._db = DB()

    def growing_avg(self, a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1 :] / n

    def is_growing(self, data):
        return np.all(np.diff(self.growing_avg(np.array(data), n=4)) > 0)

    def _get_last_rates(self, limit=7):
        sql = f"SELECT last_price FROM currency_exchange_history WHERE currency_code='{self.currency}' ORDER BY updated_at DESC LIMIT {limit}"
        return [x["last_price"] for x in self._db.execute(sql)]

    def check_currency_growing(self, percent_value_to_sell):
        currency_values = self._get_last_rates()
        status = self.is_growing(currency_values)
        trend_status = "growing" if status else "falling"
        click.echo(f"Currency ETH has trend of {trend_status}")
        if status:
            src_wallet_balance = check_ballance(main_wallet)
            click.echo(f"Source wallet value: {src_wallet_balance}")
            value_to_send = src_wallet_balance * Decimal(percent_value_to_sell / 100.0)
            click.echo(f"Value from srouce wallet value to send: {value_to_send}")
            transaction_id = make_transfer(main_wallet, trade_wallet, main_private_key, value_to_send)
            click.echo(f"Transfer finsihed, transaction id: {transaction_id}")


@click.command()
@click.option("--proceed", help="When true values calculated will be send", required=False, default=False, is_flag=True)
@click.option("--percent", help="Pecent of assets of ETH to send", required=True, type=float)
def main(percent, proceed):
    checker = AnalyzeRates("ETH")
    checker.check_currency_growing(percent)


if __name__ == "__main__":
    main()
