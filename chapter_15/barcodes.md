# install

```bash
$ pip install "python-barcode[images]"
```

# barcodes

## errors

```python
$ python barcode_example.py

Traceback (most recent call last):
  File "/Users/hubertpiotrowski/work/fun-with-python/chapter_15/barcode_example.py", line 6, in <module>
    EAN13(str(random.randint(500000, 999999)), writer=SVGWriter()).write(f)
  File "/Users/hubertpiotrowski/.virtualenvs/fun3/lib/python3.10/site-packages/barcode/ean.py", line 49, in __init__
    raise NumberOfDigitsError(
barcode.errors.NumberOfDigitsError: EAN must have 12 digits, not 6.
```

## reader

```bash
$ pip install opencv-python pyzbar
```
zbar lib install

```bash
# MacOS
$ brew install zbar
# Linux
$ sudo apt-get install libzbar0
```

# SVG to PNG

```bash
$ pip install cairosvg
```

# sharp barcode

```bash
$ pip install imutils
```
