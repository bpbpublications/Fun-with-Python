# install ndpi

```bash
$ sudo apt-get install build-essential git gettext flex bison libtool \
autoconf automake pkg-config libpcap-dev libjson-c-dev libnuma-dev libpcre2-dev libmaxminddb-dev librrd-dev
```

# nfstream

```bash
$ pip install nfstream
```

# network interfaces

```bash
$ ip a

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 34:17:eb:a4:6c:3a brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.104/24 brd 192.168.0.255 scope global dynamic eno1
       valid_lft 6453sec preferred_lft 6453sec
    inet6 fe80::3617:ebff:fea4:6c3a/64 scope link
       valid_lft forever preferred_lft forever
(...)
```

## filter

```python
ff = "tcp port 80"
my_streamer = NFStreamer(source="eno1",
   statistical_analysis=False,
   idle_timeout=1,
   bpf_filter=ff,
)
```
