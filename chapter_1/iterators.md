# iterators

Example

```python
my_numbers = [1, 2, 3, 4, 5]
data = iter(my_numbers)
print(next(data))
print(next(data))
print(next(data))
print(next(data))
print(next(data))
```

more complex

```python
class AsciiIterator:

    def __iter__(self):
        self.current_value = 65
        return self

    def __next__(self):
        if self.current_value > 90:
            raise StopIteration
        tmp_value = self.current_value
        self.current_value += 1
        return chr(tmp_value)

obj = AsciiIterator()
my_iterator = iter(obj)

for letter in my_iterator:
    print(letter, end = ",")
```

# generators

example

```python
def my_numbers():
    for i in range(1, 6):
        yield i

obj = my_numbers()
print(next(obj))
print(next(obj))
print(next(obj))
print(next(obj))
print(next(obj))
```

same as iterator

```python
def ascii_iterator():
    for i in range(65, 91):
        yield chr(i)

my_letters = ascii_iterator()

for letter in my_letters:
    print(letter, end=",")
```
