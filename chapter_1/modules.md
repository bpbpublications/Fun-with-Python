# modules

## example structure for package


```bash
sound/                          Top-level package
      __init__.py               Initialize the sound package
      formats/                  Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/                  Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```

hiding some modules `__init__.py`

```Python
__all__ = ['echo']

SOME_VARIABLE = 'abc 123'

def some_function(arg: int) -> str:
    return str(arg)
```

# intra import

```Python
from sound.filters.vocoder import foo
from ..filters.vocoder import foo
```

or

```Python
from . import echo
from .. import formats
from ..filters.vocoder import foo
```