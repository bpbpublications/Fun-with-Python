```python
from pyroute2.netlink.nfnetlink.nftsocket import NFPROTO_IPV4
from pyroute2.nftables.main import NFTables

def test_ipv4_addr_set():
    with NFTables(nfgen_family=NFPROTO_IPV4) as nft:
        nft.table("add", name="filter_1")
        my_set = nft.sets(
            "add", table="filter", name="test", key_type="ipv4_addr",
            comment="my test fw filter", timeout=0)

        nft.set_elems(
            "add",
            table="filter",
            set="test_filter",
            elements={"10.65.0.4", "10.65.0.2"},
        )
```

## with timeout

```python
from pyroute2.nftables.main import NFTSetElem

nft.set_elems(
    "add",
    set=my_set,
    elements={NFTSetElem(value="10.65.0.9", timeout=12000)},
)
```
