# standard

```Python
def foo(arg1, arg2):
    return args1 + arg2

foo(1,2)
```

with more args

```Python
def foo(*args):
    return sum(args)

foo(1,2,3,4,5,6,7,8)
```

with named args

```Python
def foo(arg1, arg2):
    return arg1 + arg2

foo(2, arg2=5)
```

with dynamic named args

```Python
def foo(arg1, arg2, **kwargs):
    return arg1 + arg2 + sum([v for v in kwargs.values()])

foo(2, arg2=5, v1=10, v2=15, v3=5)
```

with mixed args

```Python
def foo(arg1, arg2, *args, **kwargs):
    result = arg1 + arg2 + sum(args)
    if kwargs and kwargs.get('multi'):
        return result * kwargs['multi']
    return result

foo(2, 5, 1, 2 ,3, multi=10)
foo(2, 5, 1, 2 ,3, ignore_arg=123)
```

With better and cleaner types definition

```Python
from typing import List, Dict


def foo(arg1: int, arg2: int, *args: List[int], **kwargs: Dict[str, int]):
    result = arg1 + arg2 + sum(args)
    if kwargs and kwargs.get('multi'):
        return result * kwargs['multi']
    return result

value_1 = foo(2, 5, 1, 2 ,3, multi=10)
value_2 = foo(2, 5, 1, 2 ,3, ignore_arg=123)

print(value_1)
print(value_2)
```

# variables scoping

```Python
my_variable = "started with value"
def scoped_function():
    def run_global():
        global my_variable
        my_variable = "global eggs"

    def run_local():
        my_variable = "i love eggs"

    def run_nonlocal():
        nonlocal my_variable
        my_variable = "nonlocal eggs"

    my_variable = "test value"
    run_local()
    print(f"After local assignment: {my_variable}")
    run_nonlocal()
    print(f"After nonlocal assignment: {my_variable}")
    run_global()
    print(f"After global assignment: {my_variable}")

print(f"Started with value: {my_variable}")
scoped_function()
print("In global scope:", my_variable)
```


# scopes

## global

```Python
# file func1.py
def foo():
    SOME_VAR = "x"

# file func2.py
SOME_VAR = "abc"

def foo2():
    global SOME_VAR
    print(SOME_VAR)

# file func3.py
from func1 import foo
from func2 import foo2, SOME_VAR


def foo3():
    global SOME_VAR
    SOME_VAR = "here i am"

foo()
foo2()
foo3()
foo2()
foo()

print(SOME_VAR)
```
