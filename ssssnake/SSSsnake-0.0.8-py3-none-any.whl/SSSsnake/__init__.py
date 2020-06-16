from IPython.display import HTML
from IPython.display import display
from IPythonDisplayTurtle import Snake
from IPythonDisplayTurtle import ReadFile as ReadFileLib
import random
import math
import os.path

def ReadFile (filename):
    with open(os.path.join(os.path.dirname(__file__), 'levels' , filename), 'r') as myfile:
        data = myfile.read()
        return data

class SSSsnake(Snake):
    
    _unitSize = 50
    _rotationAmount = 90
    
    _homeX = 30
    _homeY = 30
    
    def __init__(self):
        super.__init__(_pendown = 0, homeX = self._homeX, homeY = self._homeY)
        
    ## Helper methods, these are the expected way to interract with the turtle
    # the SSS turtle can only move in units!
    def turnRight(self):
        self._rotateTo(self._rotation + self._rotationAmount)
        
    def turnLeft(self):
        self._rotateTo(self._rotation - self._rotationAmount)
    
    def move(self):
        newX = self._x + round(self._unitSize * math.sin(math.radians(self._rotation)), 1)
        newY = self._y - round(self._unitSize * math.cos(math.radians(self._rotation)), 1)
        self._moveTo(newX, newY)

class SSSfirstsnake (SSSsnake):
    def turnLeft (self):
        raise Exception("I don't know what this command means!")