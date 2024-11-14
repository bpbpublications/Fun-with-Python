# install

```bash
$ pip install dnslib netifaces
```

# query

```bash
$ dig @localhost -p 8953 wikipedia.org

; <<>> DiG 9.10.6 <<>> @localhost -p 8953 wikipedia.org
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 23026
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;wikipedia.org.         IN  A

;; ANSWER SECTION:
wikipedia.org.      471 IN  A   185.15.59.224
```
