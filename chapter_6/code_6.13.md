# run

## init DB

```sh
$ python code_6.13.py --operation=init

# output
Executing: CREATE TABLE IF NOT EXISTS virus_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            virus_hash TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
```

## loading data

```sh
$ python code_6.13.py --operation=import --source=example_virus_sha256.bin --source=example_virus_sha256_2.bin

# output
Importing: ('example_virus_sha256.bin', 'example_virus_sha256_2.bin')
Insert/update: INSERT OR IGNORE INTO virus_db (virus_hash) values ('ebf454d4b0d094cedf591c6dbe370c4796572a67139174da72559156dd2265ed')
Insert/update: INSERT OR IGNORE INTO virus_db (virus_hash) values ('61db3163315e6b3b08a156360812ca5efff0093234201a994d6bdedaf85afeb0')
Insert/update: INSERT OR IGNORE INTO virus_db (virus_hash) values ('1bf454d4b0d094cedf591c6dbe370c4796572a67139174da72559156dd2265e1')
Insert/update: INSERT OR IGNORE INTO virus_db (virus_hash) values ('11db3163311e6b3b08a156360812ca5efff0093234201a994d6bdedaf85afeb1')
```
