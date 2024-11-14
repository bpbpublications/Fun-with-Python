import click
import os
import requests
import sqlite3
from datetime import datetime, timedelta
from db import DB


class LiveCoinClient:
    def __init__(self):
        self.__api_token = os.environ.get("API_KEY")
        assert self.__api_token, "variable API_KEY not specified"
        self._db = DB()

    def __fetch_data(self, url):
        return requests.post(url, headers={"x-api-key": self.__api_token, "content-type": "application/json"}).json()

    def __post_data(self, url, page_limit=500, page_offset=0):
        click.echo(f"Page limit: {page_limit}, offset: {page_offset}")
        data = {
            "currency": "USD",
            "sort": "rank",
            "order": "ascending",
            "offset": page_offset,
            "limit": page_limit,
            "meta": True,
        }
        data = requests.post(
            url, headers={"x-api-key": self.__api_token, "content-type": "application/json"}, json=data
        ).json()
        if data:
            more_data = self.__post_data(url, page_limit=page_limit, page_offset=((page_offset + 1) + page_limit))
            if more_data:
                data += more_data
        return data

    def format_time(self, dt_value):
        return str(int(dt_value.timestamp())).replace(".", "")[:13].ljust(13, "0")

    def fetch_crypto(self, currency_code="BTC", days=1):
        timestamp_now = datetime.now()
        url = "https://api.livecoinwatch.com/coins/single/history"
        payload = {
            "currency": "USD",
            "code": currency_code,
            "start": self.format_time(timestamp_now - timedelta(days=days)),
            "end": self.format_time(timestamp_now),
            "meta": True,
        }
        data = requests.post(
            url, headers={"x-api-key": self.__api_token, "content-type": "application/json"}, json=payload
        ).json()
        for item in data["history"]:
            self.update_currency_exchange(currency_code, item["rate"], item["date"])

    def fetch_and_update_coins(self):
        click.echo("Starting fetching livecoin updates")
        url = "https://api.livecoinwatch.com/coins/list"
        data = self.__post_data(url)
        data_to_refresh = {item["code"]: item["rate"] for item in data}
        self.refresh(data_to_refresh)

    def refresh(self, data):
        for currency_code, currency_value in data.items():
            click.echo(f"Updating coing: {currency_code}")
            self.update_currency_exchange(currency_code, currency_value)

    def update_currency_exchange(self, currency_code, currency_value, updated_value=None):
        if not updated_value:
            updated_value = datetime.now().timestamp()
        sql = f"SELECT * FROM currency_exchange WHERE currency_code='{currency_code}'"
        result = self._db.execute(sql)
        if result:
            result = result.pop()
            if float(result["updated_at"]) <= float(updated_value):
                self.save_history(result["currency_code"], result["last_price"], updated_at=result["updated_at"])
                sql = f"UPDATE currency_exchange SET last_price='{currency_value}', updated_at={updated_value}  WHERE currency_code='{currency_code}'"
                self._db.commit(sql)
            else:
                self.save_history(result["currency_code"], result["last_price"], updated_value)
        else:
            sql = f"INSERT INTO currency_exchange (last_price, currency_code, updated_at, created_at) VALUES ('{currency_value}', '{currency_code}', {updated_value}, {updated_value})"
            self._db.commit(sql)

    def save_history(self, currency_code, currency_value, updated_at):
        try:
            sql = f"""INSERT INTO currency_exchange_history (currency_code, last_price, updated_at, created_at) VALUES ('{currency_code}', '{currency_value}', '{updated_at}', '{updated_at}')"""
            self._db.commit(sql)
        except sqlite3.IntegrityError:
            click.echo("This kind of record is aleady saved in DB")
