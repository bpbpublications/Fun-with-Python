# tests

## no tests

WHen no tests at all

```bash
$ pytest tests
========================== test session starts ===========================
platform darwin -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0
rootdir: (...)chapter_2/simple_calculator
plugins: anyio-3.7.0
collected 0 items

======================== no tests ran in 0.01s ===========================
```

## with tests

```bash
$ pytest tests
========================== test session starts ===========================
platform darwin -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0
rootdir: (...)/chapter_2/simple_calculator
plugins: anyio-3.7.0
collected 5 items

tests/test_basics.py .....    [100%]

========================= 5 passed in 0.01s ==============================
```

# build

## reqs

```sh
$ pip install build
```

## build

```sh
$ python -m build

running egg_info
writing simple_calculator.egg-info/PKG-INFO
writing dependency_links to simple_calculator.egg-info/dependency_links.txt
writing requirements to simple_calculator.egg-info/requires.txt
writing top-level names to simple_calculator.egg-info/top_level.txt
reading manifest file 'simple_calculator.egg-info/SOURCES.txt'
adding license file 'LICENSE'
writing manifest file 'simple_calculator.egg-info/SOURCES.txt'
* Building sdist...
(...)
removing build/bdist.macosx-13-arm64/wheel
Successfully built simple_calculator-0.1.0.tar.gz and simple_calculator-0.1.0-py3-none-any.whl
```

## Installation

```sh
$ pip install dist/simple_calculator-0.1.0-py3-none-any.whl
```
