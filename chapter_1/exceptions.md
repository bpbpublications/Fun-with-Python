# Exceptions

example of simple one

```Python
def foo(a, b):
    print(a/float(b))

print(foo(1, 2))
print(foo(1, 0))
```

crash

```Python
0.5
None

---

ZeroDivisionError Traceback (most recent call last)
Cell In [31], line 5
2 print(a/float(b))
4 print(foo(1, 2))
----> 5 print(foo(1, 0))

Cell In [31], line 2, in foo(a, b)
1 def foo(a, b):
----> 2 print(a/float(b))

ZeroDivisionError: float division by zero
```

improved code

```Python
def foo(a, b):
    try:
        return (a/float(b))
    except ZeroDivisionError:
        print("We don't know how to devide by zero")
    except Exception as e:
        print(f"Something unexpected happened, details: {e}")

print(foo(1, 2))
print(foo(1, 0))
print(foo(1, "lalala"))
```

checking parameters and raising exception

```Python
def foo(a, b):
    assert isinstance(a, (int, float)), "Argument 2 must be number"
    assert isinstance(b, (int, float)), "Argument b must be number"

    if b < 0:
        raise Exception("Sorry but 2nd argument must be greater than zero")

    return (a/float(b))
```


```Python
print(foo(1, 2))
print(foo(1, -1))
print(foo(1, 0))
print(foo(1, "lalala"))
```