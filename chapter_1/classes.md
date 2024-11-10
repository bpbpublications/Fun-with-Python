# definition


## basic usage

```Python
class Point:
    x: int
    y: int
```

execute

```
p = Point()
p.x = 20
p.y = 15
```

## pseudo import

```Python
from super.awesome.module import caller
from another.awesome.module import stuff

p1 = stuff.Point()
p1 = caller.Point()
```

wrong use of namespaces

```Python
from super.awesome.module.caller import Point
from another.awesome.module.stuff import Point

p1 = Point()
p1 = Point()
print(p1 == p2)  # False
print(isinstance(p1, Point))  # True
print(isinstance(p2, Point))  # True
```


compare classes namespaces

```Python
class Point:
    x: int
    y: int

p1 = Point()
p1.x = 10
p1.y = 5

p2 = Point()
p2.x = 10
p2.y = 5

print(p1 == p2)  # False
print(isinstance(p1, Point))  # True
print(isinstance(p2, Point))  # True

# clean code

```Python
import pickle
from collections.abc import Callable
from typing import NewType

MyObject = NewType('UserId', Callable[[], str])


class Serializer(object):

    def __init__(self, compression=False, compression_level=6, use_zlib: bool=False,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL):
        """
        Initializer, expected arguments:
        - compression - True, means zip compression is going to be used
        - compression_level - compresson level
        - use_zlib - True, means using zlib library
        """
        self.comp = compression
        self.comp_level = compression_level
        self.use_zlib = use_zlib
        self.pickle_protocol = pickle_protocol or pickle.HIGHEST_PROTOCOL
        if self.comp:
            if self.use_zlib and zlib is None:
                raise ConfigurationError('use_zlib specified, but zlib module '
                                         'not found.')
            elif gzip is None:
                raise ConfigurationError('gzip module required to enable '
                                         'compression.')

    def _serialize(self, data: str) -> str:
        """Serialize given data to pickle reprezentation"""
        return pickle.dumps(data, self.pickle_protocol)

    def _deserialize(self, data: str) -> Callable[[], str]:
        """Deserialize pickled object to its original state"""
        return pickle.loads(data)

    def serialize(self, data: Callable[[], str]):
        data = self._serialize(data)
        if self.comp:
            if self.use_zlib:
                data = zlib.compress(data, self.comp_level)
            else:
                data = gzip_compress(data, self.comp_level)
        return data

    def deserialize(self, data: MyObject) -> str:
        if self.comp:
            if not is_compressed(data):
                logger.warning('compression enabled but message data does not '
                               'appear to be compressed.')
            elif self.use_zlib:
                data = zlib.decompress(data)
            else:
                data = gzip_decompress(data)
        return self._deserialize(data)
```

Usage

```Python
data = {"key1": "some value"}
s = Serializer()
serialized_data = s.serialize(data)
s.deserialize(serialized_data)
```

# Constructor

## Lazy

```Python
class Foo:

    def __init__(self, arg1, arg2):
        self.argument_1 = arg1
        self.argument_2 = arg2
        self.print_me()

    def print_me(self):
        """Example printing of constructor args"""
        print(f"argument 1: {self.argument_1}")
        print(f"argument 2: {self.argument_2}")
```

## Non lazy

```Python
class Foo:

    argument_1 = 5
    argument_2 = 6

    def __init__(self, arg1, arg2):
        self.print_me()
        self.argument_1 = arg1
        if arg2 > self.argument_2:
            self.argument_2 = arg2
        self.print_me()

    def print_me(self):
        """Example printing of constructor args"""
        print(f"argument 1: {self.argument_1}")
        print(f"argument 2: {self.argument_2}")
```

assign and overwrite attributes

```Python
f = Foo(10, 15)
argument 1: 10
argument 2: 15

f.print_me()
argument 1: 10
argument 2: 15

f.argument_1 = 30
f.argument_2 = 40
f.print_me()

argument 1: 30
argument 2: 40
```
## protected argument

```Python
class Foo:

    def __init__(self, arg1, arg2):
        self._argument_1 = arg1
        self._argument_2 = arg2
        self.print_me()

    def print_me(self):
        """Example printing of constructor args"""
        print(f"argument 1: {self._argument_1}")
        print(f"argument 2: {self._argument_2}")
```

Listings proteted arguments

```Python
f = Foo(5,7)
dir(f)
```

## private attributes

```Python
class Foo:

    def __init__(self, arg1, arg2):
        self.__argument_1 = arg1
        self.__argument_2 = arg2
        self.__print_me()

    def __print_me(self):
        """Example printing of constructor args"""
        print(f"argument 1: {self.__argument_1}")
        print(f"argument 2: {self.__argument_2}")
```

## destructor

```Python
class Foo:

    def __init__(self, arg1, arg2):
        self.__argument_1 = arg1
        self.__argument_2 = arg2
        self.__print_me()

    def __print_me(self):
        """Example printing of constructor args"""
        print(f"argument 1: {self.__argument_1}")
        print(f"argument 2: {self.__argument_2}")

    def __del__(self):
        self.__argument_1 = None
        self.__argument_2 = None
        print('bye bye!')
```

destroy it

```Python
f = Foo(1, 5)
del(f)
```
