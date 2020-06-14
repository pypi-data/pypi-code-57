import os

def display(cls):
    d = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print(open(d + "/roebuck.txt").read())
