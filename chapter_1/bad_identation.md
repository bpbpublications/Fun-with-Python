example of bad identation

```python
import urllib
from urllib import parse as urlparse

def parse_qsl_to_dict(value):
    """
    Returns a dict from a querystring-encoded string.
    """
    return dict(urlparse.parse_qsl(value, keep_blank_values=True))

class BasiceService(BaseHTTPRequestHandler):
    def read_body(self):
        # some comment
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)

    def dummy_function(self, *args):
        if args and len(args)> 0:
            return True
        else:
          return False
        return 1
```
