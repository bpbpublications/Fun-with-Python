# analyze

```python
import time
import petalock

class VirusScanner:

    def __init__(self):
        self.locks = {}
        self.files_to_lock = []
        self.files_to_remove_lock = []

    def _remove_lock(self, file_path):
        petalock.unlock(self.locks[file_path])
        self.locks[file_path].close()
        del self.locks[file_path]

    def _create_lock(self, file_path):
        with open(file_path, 'a+') as f:
            f.seek(0)
            self.locks[file_path] = f

    def analyze_locks(self):
        while True:
            while self.files_to_lock:
                self._create_lock(self.files_to_lock.pop())
            while self.files_to_remove_lock:
                self._remove_lock(self.files_to_remove_lock.pop())
            time.sleep(1)


        print(f'Finished creating and analyzing locks')
```

improved

```python
def _create_lock(self, file_path):
    if file_path not in self.locks:
        with open(file_path, 'a+') as f:
            f.seek(0)
            self.locks[file_path] = f
```
