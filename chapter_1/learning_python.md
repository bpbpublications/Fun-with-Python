# Fibonacci series

```python
a, b = 0, 1
while a < 10:
    print(a)
    a, b = b, a+b
```

# loop


## Simple loops

```python
def hello_world(message):
    print(message)

for x in range(10):
    hello_world(f"repeat {x}")
```

with conditions beings used

```python
def hello_world(message):
    print(message)

for x in range(10):
    if x % 2 == 0:
        y = x * 2
        hello_world(f"value {y}")
```
