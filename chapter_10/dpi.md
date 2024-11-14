# packet

```python
NFlow(id=30,
    expiration_id=0,
    src_ip=192.168.0.104,
    src_mac=34:17:eb:a4:6c:3a,
    src_oui=34:17:eb,
    src_port=46181,
    dst_ip=1.0.0.1,
    dst_mac=78:8c:b5:ae:07:c2,
    dst_oui=78:8c:b5,
    dst_port=53,
    protocol=17,
    ip_version=4,
    vlan_id=0,
    (...)
    application_name=DNS.Google,
    application_category_name=Network,
    requested_server_name=google.com,
)
```

## http

```python
NFlow(
    src_ip=192.168.0.104,
    src_mac=34:17:eb:a4:6c:3a,
    src_oui=34:17:eb,
    src_port=51684,
    dst_ip=80.72.192.41,
    dst_mac=78:8c:b5:ae:07:c2,
    dst_oui=78:8c:b5,
    dst_port=80,
    protocol=6,
    ip_version=4,
    vlan_id=0,
    tunnel_id=0,
    (..)
    application_name=HTTP,
    application_category_name=Web,
    requested_server_name=inet.pl,
    user_agent=curl/7.68.0,
    content_type=text/html
)
```

# firewall

```bash
$ pip install pyroute2
```

# mime


```python
BLOCKED_MIME_TYPES = ['video/x-msvideo', 'video/mp4']

def filter_blacklist(frame):
    if frame.requested_server_name.strip() in BLACKLIST and frame.dst_ip not in BLACKLIST_IPS:
        if frame.content_type in BLOCKED_MIME_TYPES:
            print(f'blacklisted {frame.requested_server_name}')
            BLACKLIST_IPS.append(frame.dst_ip)
            dump_ips()
```
