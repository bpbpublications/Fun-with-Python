# installation

```bash
$ pip install O365
```

#configure

https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Authentication/

# execute

```bash
python office_tester.py --client-id <retried client id> --secret <retrienve client secret>
events:

Subject: <some event 1> (on: 2023-08-30 from: 16:15:00 to: 16:55:00)
Subject: <some event 2> (on: 2022-09-11 from: 18:00:00 to: 18:30:00)
```

## load settings

```pythhon
config = configparser.ConfigParser()
config.read("sync.ini")
```
