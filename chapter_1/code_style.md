# bad

```python
def FoO(ARgINt8):
    myTmpV = ARgINt8 * 20
    return OtherFoO2(myTmpV/2)
def OtherFoO2(ARgINt8):
    return ARgINt8*0.1
if __name__ == "__main__":
    print(FoO())
```

# good

same as above but good


```python
def simple_calculator(in_multiplier):
    """This is pretty simple function that deliver some math."""
    my_temp_var = in_multiplier * 20
    return moving_comma(my_temp_var/2)


def moving_comma(data):
    return data*0.1


if __name__ == "__main__":
    print(simple_calculator())
```
