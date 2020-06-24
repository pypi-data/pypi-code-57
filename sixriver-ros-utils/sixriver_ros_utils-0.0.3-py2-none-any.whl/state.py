#!/usr/bin/python
import math



def wrapAngle(angle):
    while angle >  math.pi:
        angle -= 2 * math.pi
    while angle <= -math.pi:
        angle += 2 * math.pi
    return angle



class State:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self):
        return "[pos: [{}, {}, {}]]".format(
            self.x, self.y, self.theta)

    def __repr__(self):
    	return str(self)

    def transform(self, p):
        return State(
            self.x + p.x * math.cos(self.theta) - p.y * math.sin(self.theta),
            self.y + p.x * math.sin(self.theta) + p.y * math.cos(self.theta),
            wrapAngle(self.theta + p.theta))
    def rotate(self, angle):
    	return State(self.x * math.cos(angle) - self.y * math.sin(angle), 
    		self.x * math.sin(angle) + self.y * math.cos(angle),
    		self.theta + angle)
    def translate(self, x, y):
    	return State(self.x + x, 
    		self.y + y,
    		self.theta)

    def inverse(self):
        return State(
            -self.x * math.cos(self.theta) - self.y * math.sin(self.theta),
            -self.y * math.cos(self.theta) + self.x * math.sin(self.theta),
            wrapAngle(-self.theta))