class MyCalculator:

    def __init__(self, x):
        self.x = x

    def add_me(self, y):
        return self.x + y

    def substract_me(self, y):
        return self.x - y

    def divide_me(self, y):
        if y != 0:
            return self.x / float(y)
        raise Exception('Hey hey, 2nd argument can not be 0')

    def multiple_me(self, y):
        return self.x * y
