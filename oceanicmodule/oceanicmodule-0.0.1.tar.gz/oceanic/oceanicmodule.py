class Oceanic:

    def __init__(self, name, movement="moving"):
        self.name = name
        self.movement = movement

    def move(self):
        return "{} is {}".format(self.name, self.movement)


class Fish(Oceanic):

    def __init__(self, name, movement="swimming"):
        self.name = name
        self.movement = movement

    def swim(self):
        return "{} is swimming".format(self.name)


class Octopus(Oceanic):

    def __init__(self, name, movement="crawling"):
        self.name = name
        self.movement = movement

    def move(self):
        return "{} is crawling from base class".format(self.name)


def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()


def fib2(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result
