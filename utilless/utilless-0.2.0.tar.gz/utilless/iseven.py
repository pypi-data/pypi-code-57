"Module iseven"


def iseven(num):
    """Infamous function that checks if a number is even.
    Let's face it: you need to learn how to use modulo (%)"""

    if not isinstance(num, int):
        raise TypeError("Not an integer, so cannot check if even")

    return num % 2 == 0
