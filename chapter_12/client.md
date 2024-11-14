# run client with no server


```sh
$ python udp_client.py
Traceback (most recent call last):
  File "udp_client.py", line 9, in <module>
    data = s.recv(1024)
ConnectionRefusedError: [Errno 61] Connection refused
```

# error catching

```bash
$ python tcp_client_1.py

Connection error code 61
```

## execute


### linear

```bash
$ time python tcp_port_scanner_linear.py

{25: False, 80: True, 443: True}

python tcp_port_scanner_linear.py  0.04s user 0.02s system 33% cpu 0.176 total
```

### syncio

```bash
$ time python tcp_port_scanner.py

[Errno 61] Connect call failed ('185.15.59.224', 25)
{443: True, 80: True, 25: False}
python tcp_port_scanner.py  0.06s user 0.03s system 51% cpu 0.180 total
```

# many sites

```bash
$ python scanner.py
[Errno 61] Connect call failed ('185.15.59.224', 25)
[Errno 61] Connect call failed ('142.250.186.206', 25)
{'google.com': {25: False, 80: True, 443: True},
 'wikipedia.org': {25: False, 80: True, 443: True}}
```

# ping

```bash
$ pip install ping3
```

result

```bash
$ python ping_test.py --host wikipedia.org
Response time 0.10447406768798828s
```


# site status

```bash
$ python check_site_status.py --url https://wikipedia.org

Site status: True
```

# YAML

```bash
$ pip install PyYAML
```

# asyncping

```bash
$ pip install aioping
```

# async scannner

```bash
$ python scanner2.py --config config.yaml

result: {'gmail.com': {443: True,
               465: False,
               587: False,
               'ping': 10.923624999122694,
               'status': True},
 'vimeo.com': {80: True, 443: True, 'ping': 13.128791993949562, 'status': True},
 'wikipedia.org': {80: True,
                   443: True,
                   465: False,
                   'ping': 33.38837499904912,
                   'status': True}}
```
