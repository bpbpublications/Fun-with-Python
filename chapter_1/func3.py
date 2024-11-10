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

