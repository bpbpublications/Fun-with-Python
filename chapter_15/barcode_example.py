import random
from barcode import EAN13
from barcode.writer import SVGWriter

with open("/tmp/somefile.svg", "wb") as f:
    EAN13(str(random.randint(111122221111, 666677779999)), writer=SVGWriter()).write(f)
