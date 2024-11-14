# import

```python
$ python code_7.6.py
```

result

```bash
...
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('ZEN', 'Horizen');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('BTRST', 'Braintrust');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('TRAC', 'OriginTrail');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('RBN', 'Ribbon Finance');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('HFT', 'Hashflow');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('METIS', 'MetisDAO');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('JOE', 'JOE');
Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('AXL', 'Axelar');
Inserted 200 items
```

crash

```bash
$ python code_7.6.py


Insert/update: INSERT INTO currency(currency_code, currency_name) VALUES ('BTC', 'Bitcoin');
Traceback (most recent call last):
  File "code_7.6.py", line 27, in <module>
    no_items = main()
  File "code_7.6.py", line 20, in main
    db.commit(sql)
  File "/Users/hubertpiotrowski/work/fun-with-python/chapter_7/db.py", line 20, in commit
    cursor.execute(sql)
sqlite3.IntegrityError: UNIQUE constraint failed: currency.currency_code
```
