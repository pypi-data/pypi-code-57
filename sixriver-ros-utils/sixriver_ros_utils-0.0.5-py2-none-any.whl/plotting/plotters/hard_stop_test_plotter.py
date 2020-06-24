#!/usr/bin/python
import matplotlib.pyplot as plt
from plot_utils import ConversionUtils
import rospy
import math
import numpy as np

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

class PosePlotter:
    def __init__(self):
        self.x = []
        self.y = []
        self.theta = []
        self.t = []
        self.t_stamp = []
        self.dw = []
        self.dv = []

        self.t_test = []
        self.x_test = []
        self.y_test = []
        self.dv_test = []
        self.dw_test = []
        self.theta_test = []

        self.start_pose = None
        self.end_pose = None
        self.end_pose_rel = None
        self.test_active = False

        self.topic = ["/corner_detector/corner_detection_inverse"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.x.append(msg.pose.pose.position.x)
            self.y.append(msg.pose.pose.position.y)
            self.theta.append(ConversionUtils.quat2Yaw(msg.pose.pose.orientation))
            (dv, dw) = self.build_diff_velocities_from_last()
            self.dw.append(dw)
            self.dv.append(dv)

            if self.test_active:
                # During the test.  Store data
                original = self.build_state_from_last()
                relative = self.start_pose.inverse().transform(original)
                self.t_test.append(relative.t)
                self.x_test.append(relative.x)
                self.y_test.append(relative.y)
                self.theta_test.append(relative.theta)

                (dv, dw) = self.build_diff_velocities_from_last()
                self.dw_test.append(dw)
                self.dv_test.append(dv)


    def mark_start(self):
        self.test_active = True
        self.start_pose = self.build_state_from_last()
        self.t_test.append(self.start_pose.t)
        self.x_test.append(0)
        self.y_test.append(0)
        self.theta_test.append(0)
        (dv, dw) = self.build_diff_velocities_from_last()
        self.dw_test.append(dw)
        self.dv_test.append(dv)

        return self.start_pose.t



    def mark_end(self):
        self.test_active = False
        self.end_pose = self.build_state_from_last()
        self.end_pose_rel = self.start_pose.inverse().transform(self.end_pose)


    def build_state_from_last(self):
        try:
            return State(
                self.x[-1], self.y[-1], self.theta[-1],
                0, 0, self.t_stamp[-1])
        except:
            return State(0, 0, 0, 0, 0, 0)

    def build_diff_velocities_from_last(self):
        try:
            dx = self.x[-1] - self.x[-2]
            dy = self.y[-1] - self.y[-2]
            dt = self.t_stamp[-1] - self.t_stamp[-2]
            dv = math.sqrt(dx * dx + dy * dy) / dt
            dtheta = ConversionUtils.clampAngle(self.theta[-1] - self.theta[-2])
            dw = dtheta / dt
            return (dv, dw)
        except:
            return (0, 0)


    def plot(self, fignum):
        pass


class OdometryPlotter:
    def __init__(self):
        self.v = []
        self.w = []
        self.x = []
        self.y = []
        self.dv = []
        self.dw = []
        self.theta = []
        self.t = []
        self.t_stamp = []

        self.t_test = []
        self.v_test = []
        self.w_test = []
        self.dv_test = []
        self.dw_test = []
        self.x_test = []
        self.y_test = []
        self.theta_test = []

        self.start_pose = None
        self.end_pose = None
        self.end_pose_rel = None
        self.test_active = False

        self.topic = ["/sensors/odometry/pose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.v.append(msg.twist.twist.linear.x)
            self.w.append(msg.twist.twist.angular.z)
            self.x.append(msg.pose.pose.position.x)
            self.y.append(msg.pose.pose.position.y)
            self.theta.append(ConversionUtils.quat2Yaw(msg.pose.pose.orientation))
            (dv, dw) = self.build_diff_velocities_from_last()
            self.dw.append(dw)
            self.dv.append(dv)


            if self.test_active:
                # During the test.  Store data
                original = self.build_state_from_last()
                relative = self.start_pose.inverse().transform(original)

                self.t_test.append(relative.t)
                self.x_test.append(relative.x)
                self.y_test.append(relative.y)
                self.theta_test.append(relative.theta)
                self.v_test.append(relative.v)
                self.w_test.append(relative.w)


                (dv, dw) = self.build_diff_velocities_from_last()
                self.dw_test.append(dw)
                self.dv_test.append(dv)


    # def mark_start(self):
    #     self.test_active = True
    #     self.start_pose = self.build_state_from_last()
    #     self.t_test.append(self.start_pose.t)
    #     self.x_test.append(0)
    #     self.y_test.append(0)
    #     self.theta_test.append(0)
    #     self.v_test.append(self.start_pose.v)
    #     self.w_test.append(self.start_pose.w)

    def mark_start(self, time):
        print "marking start at {}".format(time)
        self.test_active = True
        states = self.build_states_from_time(time)
        self.start_pose = states[0]
        print "start state: {}".format(self.start_pose)
        for original in states:
            # relative = original.transform(self.start_pose.inverse())
            relative = self.start_pose.inverse().transform(original)

            self.t_test.append(relative.t)
            self.x_test.append(relative.x)
            self.y_test.append(relative.y)
            self.theta_test.append(relative.theta)
            self.v_test.append(relative.v)
            self.w_test.append(relative.w)


            (dv, dw) = self.build_diff_velocities_from_last()
            self.dw_test.append(dw)
            self.dv_test.append(dv)


    def mark_end(self):
        self.test_active = False
        self.end_pose = self.build_state_from_last()
        self.end_pose_rel = self.start_pose.inverse().transform(self.end_pose)

    def build_state_from_last(self):
        try:
            return State(
                self.x[-1], self.y[-1], self.theta[-1],
                self.v[-1], self.w[-1], self.t_stamp[-1])
        except:
            return State(0, 0, 0, 0, 0, 0)

    def build_states_from_time(self, time):
        # Search backwards through the state to find the state that matches the time
        output = []
        k = len(self.t_stamp) - 1
        print "k = {}".format(k)
        while k > 0:
            output.append(State(
                self.x[k], self.y[k], self.theta[k],
                self.v[k], self.w[k], self.t_stamp[k]))
            if self.t_stamp[k] < time:
                break
            k -= 1

        return output[::-1]

    def build_diff_velocities_from_last(self):
        try:
            dx = self.x_test[-1] - self.x_test[-2]
            dy = self.y_test[-1] - self.y_test[-2]
            dt = self.t_test[-1] - self.t_test[-2]
            dv = math.sqrt(dx * dx + dy * dy) / dt
            dtheta = ConversionUtils.clampAngle(self.theta_test[-1] - self.theta_test[-2])
            dw = dtheta / dt
            return (dv, dw)
        except:
            return (0, 0)

    def plot(self, fignum):
        pass


class HardStopTestPlotter:
    MOTION_STATE_TOPIC = "/drivers/brainstem/cmd/set_motion_state"
    TEST_WAIT_TIME = 1.0

    def __init__(self):
        self.odometryPlt = OdometryPlotter()
        self.posePlt = PosePlotter()
        self.topics = []
        self.topics.extend(self.odometryPlt.get_topics())
        self.topics.extend(self.posePlt.get_topics())
        self.topics.extend([self.MOTION_STATE_TOPIC])

        self.hardStopTime = -1
        self.testEndTime = -1
        self.cnt = 0

    def get_topics(self):
        return self.topics
    def parse(self, topic, msg, t):
        if (topic in self.topics):
            self.odometryPlt.parse(topic, msg, t)
            self.posePlt.parse(topic, msg, t)
            if self.check_for_hard_stop(topic, msg, t):
                t_start = self.posePlt.mark_start()
                self.odometryPlt.mark_start(t_start)
            if self.check_for_end(t):
                self.odometryPlt.mark_end()
                self.posePlt.mark_end()

    def check_for_hard_stop(self, topic, msg, t):
        if self.hardStopTime > 0:
            return False
        if topic != self.MOTION_STATE_TOPIC:
            return False

        if self.cnt < 2:
            print "Returning false"
            self.cnt +=1
            return False

        if not msg.operationalState.hardStop or not msg.state:
            return False
        # Initial hard stop event
        print "Test start"
        self.hardStopTime = t.to_sec()
        return True

    def check_for_end(self, t):
        if self.testEndTime > 0:
            return False
        if self.hardStopTime < 0:
            return False

        #print "T: {}, wait: {}, hst: {}".format(t.to_sec(), self.TEST_WAIT_TIME, self.hardStopTime)
        if (t.to_sec() - self.TEST_WAIT_TIME) < self.hardStopTime:
            return False
        print "Test end"
        self.testEndTime = t.to_sec()
        return True

    def plot(self, fignum):

        # Plot relative position during test window
        plt.figure(fignum)
        ax1 = plt.subplot(311)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.x_test, 'k-*',
            self.posePlt.t_test, self.posePlt.x_test, 'r-^')
        plt.ylabel('Displacement (m/s)')
        plt.legend(['Odometry', 'Absolute'])
        plt.title("Position response")
        # Plot y data
        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.y_test, 'k-*',
            self.posePlt.t_test, self.posePlt.y_test, 'r-^')
        plt.ylabel('Displacement (m)')
        # theta
        ax3 = plt.subplot(313, sharex=ax1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.theta_test, 'k-*',
            self.posePlt.t_test, self.posePlt.theta_test, 'r-^')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (rad)')

        # Plot velocities during test window
        fignum += 1
        plt.figure(fignum)
        bx1 = plt.subplot(211)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.v_test, 'k-*',
            self.odometryPlt.t_test, self.odometryPlt.dv_test, 'b-^',
            self.posePlt.t_test, self.posePlt.dv_test, 'r-^')
        plt.ylabel('Linear velocity (m/s)')
        plt.legend(['Velocity', 'Diff odom', 'Diff pose'])
        plt.title("Velocity response")
        # Plot angular velocity data
        bx2 = plt.subplot(212, sharex=bx1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.w_test, 'k-*',
            self.odometryPlt.t_test, self.odometryPlt.dw_test, 'b-^',
            self.posePlt.t_test, self.posePlt.dw_test, 'r-^')
        plt.xlabel('Time (s)')
        plt.ylabel('Angular velocity (rad/s)')

        # Plot x-y position during test window
        fignum += 1
        plt.figure(fignum)
        cx1 = plt.subplot(111)
        plt.plot(self.odometryPlt.x_test, self.odometryPlt.y_test, 'k-*',
            self.posePlt.x_test, self.posePlt.y_test, 'r-^')
        plt.ylabel('X displacement (m)')
        plt.ylabel('Y displacement (m)')
        plt.legend(['Odometry', 'Absolute'])
        plt.title("Position response")


        # Plot velocities during the whole bag
        fignum += 1
        plt.figure(fignum)
        bx1 = plt.subplot(211)
        plt.plot(self.odometryPlt.t_stamp, self.odometryPlt.v, 'k-*',
            self.odometryPlt.t_stamp, self.odometryPlt.dv, 'b-^',
            self.posePlt.t_stamp, self.posePlt.dv, 'r-^')
        plt.ylabel('Linear velocity (m/s)')
        plt.legend(['Velocity', 'Diff odom', 'Diff pose'])
        plt.title("Velocity (whole bag)")
        # Plot angular velocity data
        bx2 = plt.subplot(212, sharex=bx1)
        plt.plot(self.odometryPlt.t_stamp, self.odometryPlt.w, 'k-*',
            self.odometryPlt.t_stamp, self.odometryPlt.dw, 'b-^',
            self.posePlt.t_stamp, self.posePlt.dw, 'r-^')
        plt.xlabel('Time (s)')
        plt.ylabel('Angular velocity (rad/s)')

        # Plot odometry position during whole time period
        # fignum += 1
        # plt.figure(fignum)
        # ax1 = plt.subplot(311)
        # plt.plot(self.odometryPlt.t_stamp, self.odometryPlt.x, 'k-*')
        # plt.ylabel('Displacement (m/s)')
        # plt.legend(['Odometry'])
        # plt.title("Odometry position")
        # # Plot y data
        # ax2 = plt.subplot(312, sharex=ax1)
        # plt.plot(self.odometryPlt.t_stamp, self.odometryPlt.y, 'k-*')
        # plt.ylabel('Displacement (m)')
        # # theta
        # ax3 = plt.subplot(313, sharex=ax1)
        # plt.plot(self.odometryPlt.t_stamp, self.odometryPlt.theta, 'k-*')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Displacement (rad)')


        # Plot absolute position during whole time period
        # fignum += 1
        # plt.figure(fignum)
        # ax1 = plt.subplot(311)
        # plt.plot(self.posePlt.t_stamp, self.posePlt.x, 'r-^',
        #     self.posePlt.t, self.posePlt.x, 'b-^')
        # plt.ylabel('Displacement (m/s)')
        # plt.legend(['Absolute'])
        # plt.title("Abolute response")
        # # Plot y data
        # ax2 = plt.subplot(312, sharex=ax1)
        # plt.plot(self.posePlt.t_stamp, self.posePlt.y, 'r-^')
        # plt.ylabel('Displacement (m)')
        # # theta
        # ax3 = plt.subplot(313, sharex=ax1)
        # plt.plot(self.posePlt.t_stamp, self.posePlt.theta, 'r-^')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Displacement (rad)')

        return fignum + 1

    def writeFile(self, fp):
        # Do the calculations here
        # We want:  - start velocity
        #           - end pose relative to start odometry
        #           - end pose relative to start corner

        fp.write("Test completed.\n")
        fp.write("Start velocity: [{}, {}] \n".format(self.odometryPlt.start_pose.v, self.odometryPlt.start_pose.w))
        fp.write("End displacement: odom: [{}, {}, {}], absolute: [{}, {}, {}]\n".format(
            self.odometryPlt.end_pose_rel.x, self.odometryPlt.end_pose_rel.y, self.odometryPlt.end_pose_rel.theta,
            self.posePlt.end_pose_rel.x, self.posePlt.end_pose_rel.y, self.posePlt.end_pose_rel.theta))
