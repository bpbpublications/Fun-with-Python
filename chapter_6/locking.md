# locking

```python
import time
import portalocker

with open('somefile', 'r+') as file:
    portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE)
    file.seek(12)
    time.sleep(10)
```

another way

```python
import portalocker

with portalocker.Lock('some-file', 'rb+', timeout=60) as fh:
    # we can execute some code here


    # flush and sync to filesystem if needed
    fh.flush()
    os.fsync(fh.fileno())
```

Explicitly unlocking is not needed in most cases but omitting it has been known to cause issues: https://github.com/AzureAD/microsoft-authentication-extensions-for-python/issues/42#issuecomment-601108266
If needed, it can be done through:

>>> portalocker.unlock(file)
```
# redis

* install

```sh
$ pip install "portalocker[redis]"
```

```Python
lock = portalocker.RedisLock('some_lock_channel_name')
```


lock

```python
import fcntl


def acquire_lock(file_name):
    f = open(file_name, 'r+')
    fcntl.flock(f, fcntl.LOCK_EX)
    return f

def release_lock(f):
    f.close()

file_descr = acquire_lock('/var/tmp/some-file.txt')

release_lock(file_descr)
```

## windows

```sh
pip install pywin32
```

## portalocker

```sh
pip install portalocker
```
