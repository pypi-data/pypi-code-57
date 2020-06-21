"Module isodd"


def isodd(num):
    """Infamous function that checks if a number is odd.
    Let's face it: you need to learn how to use modulo (%)"""

    if not isinstance(num, int):
        raise TypeError("Not an integer, so cannot check if odd")

    return num % 2 == 1
