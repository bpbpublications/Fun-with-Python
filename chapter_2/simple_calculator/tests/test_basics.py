import pytest
from simple_calculator import MyCalculator

def test_adding():
    m = MyCalculator(5)
    assert m.add_me(5) == 10

def test_substract():
    m = MyCalculator(5)
    assert m.substract_me(5) == 0

def test_divide():
    m = MyCalculator(5)
    assert m.divide_me(2) == 2.5

def test_divide_with_zero():
    m = MyCalculator(5)
    with pytest.raises(Exception) as exc:
        m.divide_me(0)
    assert str(exc.value) == 'Hey hey, 2nd argument can not be 0'

def test_multiple_me():
    m = MyCalculator(3)
    assert m.multiple_me(3) == 9