import unittest
from snakelib import timer

@timer
def func(x, y=None):
    return x * y if y else x


class TimerTestCase(unittest.TestCase):
    
    def meth(self, x, y=None):
        return func(x, y)
    
    def test_timer_func(self):
        print('saf')
        func(1, y=2)
    
    def test_timer_method(self):
        self.meth(1, y=2)


if __name__ == '__main__':
    unittest.main()