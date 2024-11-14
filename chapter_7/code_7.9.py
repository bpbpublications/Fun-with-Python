def main():
    db = DB()
    raw_data = requests.get(URL).text
    data = json.loads(JSON_DATA.findall(raw_data).pop())
    result = {}
    i = 0
    for item in json.loads(data["props"]["initialState"])["cryptocurrency"]["listingLatest"]["data"]:
        try:
            result[item[30]] = item[10]
            currency_code = item[30].strip().upper()
            currency_name = item[10].strip()
            sql = (
                f"""INSERT INTO currency(currency_code, currency_name) VALUES ('{currency_code}', '{currency_name}');"""
            )
            try:
                db.commit(sql)
            except sqlite3.IntegrityError:
                print(f"Currency {currency_code} already exists, skipping...")
            except Exception as e:
                print("Error: ", e)
            i += 1
        except KeyError:
            pass
    return i
