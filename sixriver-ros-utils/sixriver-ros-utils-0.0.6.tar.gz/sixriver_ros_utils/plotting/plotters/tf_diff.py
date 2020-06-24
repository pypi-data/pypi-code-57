#!/usr/bin/python

import rospy
import tf
import math
from plot_utils import ConversionUtils

class State:
    def __init__(self, x, y, theta, v, w, t):
        self.x = x
        self.y = y
        self.theta = theta
        self.v = v
        self.w = w
        self.t = t

    def __str__(self):
        return "[t: {}, pos: [{}, {}, {}], vel: [{}, {}]]".format(
            self.t, self.x, self.y, self.theta, self.v, self.w)

    def transform(self, p):
        return State(
            self.x + p.x * math.cos(self.theta) - p.y * math.sin(self.theta),
            self.y + p.x * math.sin(self.theta) + p.y * math.cos(self.theta),
            ConversionUtils.clampAngle(self.theta + p.theta),
            p.v, p.w, p.t)

    def inverse(self):
        return State(
            -self.x * math.cos(self.theta) - self.y * math.sin(self.theta),
            -self.y * math.cos(self.theta) + self.x * math.sin(self.theta),
            ConversionUtils.clampAngle(-self.theta),
            self.v, self.w, self.t)




if __name__ == '__main__':

    ##simple script to get diff between two tfs in the same frame


    # quat to euler conversion
    # quaternion = (
    # 0,
    # 0,
    # pose.orientation.z,
    # pose.orientation.w)

    # euler = tf.transformations.euler_from_quaternion(quaternion)
    # roll = euler[0]
    # pitch = euler[1]
    # yaw = euler[2]
    # print yaw

    first =  State(0.304749900237, -0.896760779456, -0.4787195, 0, 0, 0)
    second = State(-0.272180689093, -0.597342852311, -0.4787195, 0, 0,0)

    last = first.inverse().transform(second)

    print last.x
    print last.y
    print last.theta
