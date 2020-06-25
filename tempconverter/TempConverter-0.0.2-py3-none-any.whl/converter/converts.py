def c2f(n):
    """
    celsius to fahrenheit
    """
    try:
        f = (n * 1.8) + 32
        return f
    except TypeError:
        n = "Enter a number"
        return n

def f2c(n):
    """
    fahrenheit to celsius
    """
    try:
        c = (n - 32) / 1.8
        return c
    except TypeError:
        n = "Enter a number"
        return n

def add_temp(n):
    a = f2c(n)
    b = c2f(n)
    r = a+b
    return r