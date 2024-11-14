# install

```bash
$ pip instal pyqrcode pypng
```

## example

```python
import pyqrcode
obj = pyqrcode.create('https://www.python.org')
url.png('/tmp/qr.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
```

## MeCard

```
WIFI:S:<SSID>;T:<WEP|WPA|nopass>;P:<PASSWORD>;H:<true|false|blank>;;
```

## vCard

```
BEGIN:VCARD
VERSION:4.0
FN:John Smith
N:John;Smith;;;ing. jr,M.Sc.
BDAY:--0102
GENDER:M
EMAIL;TYPE=work:joshn.smith@fooooo.com
END:VCARD
```


extended version

```
BEGIN:VCARD
VERSION:3.0
FN;CHARSET=UTF-8:John Smith
N;CHARSET=UTF-8:Smith;JOhn;;;
GENDER:M
BDAY:19670815
ADR;CHARSET=UTF-8;TYPE=HOME:;;seasame street;amazing city;;44567;Best country
TITLE;CHARSET=UTF-8:boss
ROLE;CHARSET=UTF-8:CEO
ORG;CHARSET=UTF-8:Some work
REV:2024-07-17T23:52:02.227Z
END:VCARD
```


# with config

## YAML

```bash
$ pip install pyyaml
```

## decode

```bash
$ python read_qr_code.py

decodeing result:
b'BEGIN:VCARD\n    VERSION:4.0\n    FN;CHARSET=UTF-8:John Smith\n    N;CHARSET=UTF-8:Smith;John;;;\n    GENDER:M\n\rBDAY:19780915\n\rADR;CHARSET=UTF-8;TYPE=HOME:;;seasame street;amazing city;;123456;best country\n    TITLE;CHARSET=UTF-8:upper main boss\n    ROLE;CHARSET=UTF-8:CEO\n    ORG;CHARSET=UTF-8:best company ever\n    REV:2024-07-19T20:43:59.177Z\n    END:VCARD'
```
