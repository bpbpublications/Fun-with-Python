# format check

example program

```Python
# -_- coding: utf-8 -_-
from pprint import pprint
def łąka(p):
    pprint(p)

łąka("some message")
```

save it as `my_app.py`

## flake8

```bash
$ flake8 my_app.py
```

output

```bash
my_app.py:7:1: E305 expected 2 blank lines after class or function definition,found 1
my_app.py:8:1: W391 blank line at end of file
```

* run listed errors checks

```bash
$ flake8 --select E113,W505 my_app.py
```

* exclude some errors

```bash
$ flake8 --extend-ignore E113,W505 my_app.py
```

example config file

```ini
[flake8]
ignore = D203
exclude =
    .git,
    __pycache__
max-complexity = 10
max-line-length = 120
```

## pylint

run it

```sh
$ pylint my_app.py
```

output

```
******\******* Module my_app
my_app.py:8:0: C0305: Trailing newlines (trailing-newlines)
my_app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
my_app.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
my_app.py:4:11: C0103: Argument name "p" doesn't conform to snake_case naming style (invalid-name)
my_app.py:4:0: C2401: Function name "łąka" contains a non-ASCII character, consider renaming it. (non-ascii-name)

---

Your code has been rated at 0.00/10
```
