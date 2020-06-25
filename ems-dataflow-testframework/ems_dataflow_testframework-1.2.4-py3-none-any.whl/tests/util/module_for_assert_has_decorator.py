from tests.util.dummy_decorator import dummydec


class DecoratorDummy:

    @dummydec(103, stop_max_delay=10000, wait_fixed=1000)
    def method_with_decorator(self):
        pass

    @staticmethod
    @dummydec(multiple_by=2)
    def return_one():
        return 1

    def method_without_decorator(self):
        pass

    @dummydec(stop_max_delay=10000, wait_fixed=1000)
    def method_with_decorator_2(self):
        pass

    @dummydec(stop_max_delay=10001)
    def method_with_decorator_3(self):
        pass

    @staticmethod
    def method_with_different_decorator():
        pass
