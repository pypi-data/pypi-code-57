#!/usr/bin/python
import matplotlib.pyplot as plt
from plot_utils import ConversionUtils
import rospy
import math
import numpy as np
import csv


#use rosbag record -O odom_bag.bag /tf /sensors/odometry/velocity/cmd /sensors/odometry/pose /vrpn_client_node/optihat1/mapPose
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

    def translate(self, p):
        return State(self.x - p.x, self.y - p.y, ConversionUtils.clampAngle(self.theta),
            self.v,self.w,self.t)

    def rotate(self, p):
        return State(self.x * math.cos(-p.theta) - self.y * math.sin(-p.theta),
            self.x * math.sin(-p.theta) + self.y * math.cos(-p.theta),
            ConversionUtils.clampAngle(self.theta - p.theta),
            self.v, self.w, self.t)

class CmdPlotter:
    def __init__(self):
        self.linearx = []
        self.lineary = []
        self.linearz = []
        self.t = []
        self.angularx = []
        self.angulary = []
        self.angularz = []
        self.topic = ["/sensors/odometry/velocity/cmd"]
        self.t_stamp = []
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.linearx.append(msg.linear.x)
            self.lineary.append(msg.linear.y)
            self.linearz.append(msg.linear.z)
            self.angularx.append(msg.angular.x)
            self.angulary.append(msg.angular.y)
            self.angularz.append(msg.angular.z)
    def plot(self, fignum):
        pass

class OdometryPlotter:

    start_pose = None
    end_pose = None

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

        self.charger_pose = None

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

    def relativeToFirst(self):
        # Iterate over the saved data for the hs time.
        test_k = 0
        pose_k = None
        for k in xrange(len(self.t_stamp)):
            pose_k = State(
                    self.x[k], self.y[k], self.theta[k],
                    self.v[k], self.w[k], self.t_stamp[k])
            if (k < len(self.t_stamp) - 2 and
                self.t_stamp[k + 1] > 0 and
                self.start_pose is None):
                # The previous value is the one we want
                # For now, do no interpolation
                self.start_pose = pose_k
                test_k = 0

            if self.start_pose is not None:
                # Start building the values
                original = pose_k
                relative = self.start_pose.inverse().transform(original)
                self.t_test.append(relative.t)
                self.x_test.append(relative.x)
                self.y_test.append(relative.y)
                self.theta_test.append(relative.theta)
                self.v_test.append(relative.v)
                self.w_test.append(relative.w)
                self.dv_test.append(self.dv[k])
                self.dw_test.append(self.dw[k])
        self.end_pose = pose_k
        self.end_pose_rel = self.start_pose.inverse().transform(self.end_pose)

        print self.end_pose_rel.x
        print self.end_pose_rel.y
        charger_pose1 = State(
                    0.3, 0, 0,
                    0, 0, 0)
        self.charger_pose = self.end_pose_rel.transform(charger_pose1)
        print self.charger_pose.x
        print self.charger_pose.y
        return self.start_pose.t

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



class OptitrackPlotter:

    start_pose = None
    end_pose = None

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

        self.charger_pose = None

        self.topic = ["/vrpn_client_node/optihat1/mapPose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.x.append(msg.pose.position.x)
            self.y.append(msg.pose.position.y)
            self.theta.append(ConversionUtils.quat2Yaw(msg.pose.orientation))
            (dv, dw) = self.build_diff_velocities_from_last()
            self.dw.append(dw)
            self.dv.append(dv)

    def relativeToFirst(self):
        # Iterate over the saved data for the hs time.
        test_k = 0
        pose_k = None
        for k in xrange(len(self.t_stamp)):
            pose_k = State(
                    self.x[k], self.y[k], self.theta[k],
                    0, 0, self.t_stamp[k])
            if (k < len(self.t_stamp) - 2 and
                self.t_stamp[k + 1] > 0 and
                self.start_pose is None):
                # The previous value is the one we want
                # For now, do no interpolation
                self.start_pose = pose_k
                test_k = 0

            if self.start_pose is not None:
                # Start building the values
                original = pose_k
                relative = self.start_pose.inverse().transform(original)
                self.t_test.append(relative.t)
                self.x_test.append(relative.x)
                self.y_test.append(relative.y)
                self.theta_test.append(relative.theta)
                self.dv_test.append(self.dv[k])
                self.dw_test.append(self.dw[k])
        self.end_pose = pose_k
        self.end_pose_rel = self.start_pose.inverse().transform(self.end_pose)

        print self.end_pose_rel.x
        print self.end_pose_rel.y
        charger_pose1 = State(
                    0.3, 0, 0,
                    0, 0, 0)
        self.charger_pose = self.end_pose_rel.transform(charger_pose1)
        print self.charger_pose.x
        print self.charger_pose.y

        print ("Max value: ",max(self.y_test))
        return self.start_pose.t


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


class DockingPlotter:
    def __init__(self):
        self.odometryPlt = OdometryPlotter()
        #self.cmdPlt = CmdPlotter()
        #self.optiPlt = OptitrackPlotter()
        self.topics = []
        self.topics.extend(self.odometryPlt.get_topics())
        #self.topics.extend(self.cmdPlt.get_topics())
        #self.topics.extend(self.optiPlt.get_topics())

        self.cnt = 0

    def get_topics(self):
        return self.topics
    def parse(self, topic, msg, t):
        if (topic in self.topics):
            self.odometryPlt.parse(topic, msg, t)
            self.cmdPlt.parse(topic, msg, t)
            #self.optiPlt.parse(topic, msg, t)

    def convert_data(self):
        self.odometryPlt.relativeToFirst()
        #self.optiPlt.relativeToFirst()
        return True


    def plot(self, fignum):
        if not self.convert_data():
            return
        print "Using Docking plotter"
        # Plot relative position during test window
        plt.figure(fignum)
        ax1 = plt.subplot(311)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.x_test, 'k-*')
        plt.ylabel('Displacement (x)')
        plt.legend(['Odometry'])
        plt.title("Position response")
        # Plot y data
        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.y_test, 'k-*')
        plt.ylabel('Displacement (y)')
        # theta
        ax3 = plt.subplot(313, sharex=ax1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.theta_test, 'k-*')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (rad)')

        # Plot velocities during test window
        fignum += 1
        plt.figure(fignum)
        bx1 = plt.subplot(211)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.v_test, 'k-*',
            self.odometryPlt.t_test, self.odometryPlt.dv_test, 'b-^')
        plt.ylabel('Linear velocity (m/s)')
        plt.legend(['Velocity', 'Diff odom'])
        plt.title("Velocity response")
        # Plot angular velocity data
        bx2 = plt.subplot(212, sharex=bx1)
        plt.plot(self.odometryPlt.t_test, self.odometryPlt.w_test, 'k-*',
            self.odometryPlt.t_test, self.odometryPlt.dw_test)
        plt.xlabel('Time (s)')
        plt.ylabel('Angular velocity (rad/s)')

        # Plot x-y position during test window
        fignum += 1
        plt.figure(fignum)
        cx1 = plt.subplot(111)
        plt.plot(self.odometryPlt.x_test, self.odometryPlt.y_test, 'k-*')
        #plt.plot(self.optiPlt.x_test, self.optiPlt.y_test, 'r-*')
        plt.plot(self.odometryPlt.charger_pose.x, self.odometryPlt.charger_pose.y, 'b-^')
        plt.xlabel('X displacement (m)')
        plt.ylabel('Y displacement (m)')
        plt.legend(['Odometry'])
        plt.title("Position Top Down Response")
        plt.xlim(0,1.1)
        plt.ylim(-.1, .1)   

        return fignum + 1

    def writeFile(self, fp):
        # Do the calculations here
        # We want:  - start velocity
        #           - end pose relative to start odometry
        #           - end pose relative to start corner

        fp.write("Test completed.\n")
        fp.write("Start velocity: [{}, {}] \n".format(self.odometryPlt.start_pose.v, self.odometryPlt.start_pose.w))
        fp.write("End displacement: odom: [{}, {}, {}]".format(
            self.odometryPlt.end_pose_rel.x, self.odometryPlt.end_pose_rel.y, self.odometryPlt.end_pose_rel.theta))

    def writeCsv(self, fp):
        # Do the calculations here
        # We want:  - start velocity
        #           - end pose relative to start odometry
        #           - end pose relative to start corner
        np_c_t_test=np.array(self.cmdPlt.t)
        np_c_lx_test=np.array(self.cmdPlt.linearx)
        np_c_ly_test=np.array(self.cmdPlt.lineary)
        np_c_az_test=np.array(self.cmdPlt.angularz)

        np_o_t_test=np.array(self.odometryPlt.t_test)
        np_o_x_test=np.array(self.odometryPlt.x_test)
        np_o_y_test=np.array(self.odometryPlt.y_test)
        np_o_theta_test=np.array(self.odometryPlt.theta_test)
        
        dataArrayCmd = np.vstack([np_c_t_test, np_c_lx_test])
        dataArrayCmd = np.vstack([dataArrayCmd, np_c_ly_test])
        dataArrayCmd = np.vstack([dataArrayCmd, np_c_az_test])

        dataArrayOdom = np.vstack([np_o_t_test, np_o_x_test])
        dataArrayOdom = np.vstack([dataArrayOdom, np_o_y_test])
        dataArrayOdom = np.vstack([dataArrayOdom, np_o_theta_test])

        with fp as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(dataArrayCmd)
            csvWriter.writerows(dataArrayOdom)
