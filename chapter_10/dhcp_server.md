# installation

```sh
$ git clone git@github.com:darkman66/micropython-captive-dhcp-server.git
```

# DB

## create

```shell
$ mysql -h localhost -uroot

mysql> CREATE DATABASE IF NOT EXISTS dhcp_service;
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql>
```

# initialize sqlalchemy

```python
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@localhost/dhcp_service")
```

# alembic

```bash
$ pip install alembic
$ alembic init --template generic ./scripts

```

update settings `alembic.ini`

```
sqlalchemy.url = mysql+pymysql://root@localhost/dhcp_service
```

create migration

```bash
$ alembic revision -m "create user leaese table"
```

file
```
$ alembic/versions/4944b164709d_create_user_lease_table.py
```

migration body

```python
"""create user leae table

Revision ID: 4944b164709d
Revises:
Create Date: 2023-11-19 23:04:53.414219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4944b164709d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_lease",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ip_addr", sa.String(50), nullable=False),
        sa.Column("mac_address", sa.String(50)),
    )


def downgrade() -> None:
    op.drop_table("user_lease")
```

upgrade

```bash
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
(..)
```

datetime columns

```bash
$ alembic revision -m "add datetime columns"
```

content

```python
"""add datetime columns

Revision ID: b0b4ac080f74
Revises: 4944b164709d
Create Date: 2023-11-19 23:55:45.972206

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b0b4ac080f74"
down_revision: Union[str, None] = "4944b164709d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_lease", sa.Column("created_at", sa.DateTime, default=datetime.now))
    op.add_column("user_lease", sa.Column("updated_at", sa.DateTime, default=datetime.now))


def downgrade() -> None:
    pass
```


# DHCP server

## syntax for IP

```python
Ip.next_ip(server_ip)
```

## server

```python
class CaptiveDhcpServer:

    async def run(self, server_ip: str, netmask: str):
        await self.get_leases()
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        bound = False
        while not bound:
            try:
                addr = socket.getaddrinfo("0.0.0.0", 67, socket.AF_INET, socket.SOCK_DGRAM)[0][-1]
                udps.bind(addr)
                logging.info("Starting server on port 67")
                bound = True
            except Exception as e:
                logging.error(f"Failed to bind to port {e}")
                time.sleep(0.5)


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    run_app = CaptiveDhcpServer()
    asyncio.run(run_app.run("10.65.4.1", "255.255.0.0"))
```


# add whitelist record


```python
from sqlalchemy.orm import Session
from models import WhiteListLease
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@localhost/dhcp_service")
with Session(engine) as session:
    obj = WhiteListLease(mac_address="123456789abc")
    session.add(obj)
    session.commit()
```

## error

```python
(...)
--> 143 raise errorclass(errno, errval)

IntegrityError: (pymysql.err.IntegrityError) (1062, "Duplicate entry '123456789abc' for key 'white_list_lease.mac_address'")
[SQL: INSERT INTO white_list_lease (mac_address, created_at, updated_at) VALUES (%(mac_address)s, %(created_at)s, %(updated_at)s)]
[parameters: {'mac_address': '123456789abc', 'created_at': datetime.datetime(2023, 12, 13, 8, 59, 46, 511293), 'updated_at': datetime.datetime(2023, 12, 13, 8, 59, 46, 511301)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)

In [10]: with Session(engine) as session:
    obj = WhiteListLease(mac_address="123456789abc")
    session.add(obj)
    session.commit()
```

# requests

```bash
$ pip install requests
```
