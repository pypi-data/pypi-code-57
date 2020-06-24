#!/usr/bin/python

from tf.transformations import euler_from_quaternion
import numpy as np
import rosbag
import argparse
import sys
import pdb
import csv

class ConversionUtils:
    @staticmethod
    def quat2Yaw(quat):
        orientation_list = [quat.x, quat.y, quat.z, quat.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw
    @staticmethod
    def clampAngle(angle):
        while (angle >= np.pi):
            angle -= np.pi
        while (angle < -np.pi):
            angle += np.pi
        return angle

class WheelRotationWriter:
    def __init__(self):
        self.leftCnt = []
        self.rightCnt = []
        self.leftSpd = []
        self.rightSpd = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/wheel_rotation"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            scale = 1#4096 * 10
            self.t.append(t)
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.leftCnt.append(msg.leftWheelAbsRotationCount * scale)
            self.rightCnt.append(msg.rightWheelAbsRotationCount * scale)
            if (len(self.leftCnt) > 1):
                leftSpd = (self.leftCnt[-1] - self.leftCnt[-2]) #/ (self.t_stamp[-1] - self.t_stamp[-2])
                self.leftSpd.append(leftSpd)
            else:
                self.leftSpd.append(0)
            if (len(self.rightCnt) > 1):
                rightSpd = (self.rightCnt[-1] - self.rightCnt[-2]) #/ (self.t_stamp[-1] - self.t_stamp[-2])
                #if rightSpd > 0.001:
                #    print "-1: {}, -2: {}, spd: {}".format(self.rightCnt[-1], self.rightCnt[-2], rightSpd)
                self.rightSpd.append(rightSpd)
            else:
                self.rightSpd.append(0)           
    def writeCSV(self, prefix):
        print "Writing WheelRotation to file"
        with open('{}_wheel_rotation.csv'.format(prefix), 'w+') as f:
            f.write("%time, left_wheel_rotation, right_wheel_rotation\n")
            for k in range(len(self.t_stamp)):
                f.write("{}, {}, {}\n".format(self.t_stamp[k], self.leftCnt[k], self.rightCnt[k]))

class AmclPoseWriter:
    def __init__(self):
        self.amcl_x = []
        self.amcl_y = []
        self.amcl_theta = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/amcl_pose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t)
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.amcl_x.append(msg.pose.pose.position.x)
            self.amcl_y.append(msg.pose.pose.position.y)
            self.amcl_theta.append(ConversionUtils.quat2Yaw(msg.pose.pose.orientation))
    def writeCSV(self, prefix):
        print "Writing AMCLPose to file"
        with open('{}_amcl_pose.csv'.format(prefix), 'w+') as f:
            f.write("%time, x, y, theta\n")
            for k in range(len(self.t_stamp)):
                f.write("{}, {}, {}, {}\n".format(self.t_stamp[k], self.amcl_x[k], self.amcl_y[k], self.amcl_theta[k]))

class IMUWriter:
    def __init__(self):
        self.t = []
        self.t_stamp = []
        self.orientation_x = []
        self.orientation_y = []
        self.orientation_z = []
        self.orientation_w = []
        self.orientation_covariance = []
        self.angular_velocity_x = []
        self.angular_velocity_y = []
        self.angular_velocity_z = []
        self.angular_velocity_covariance = []
        self.linear_acceleration_x = []
        self.linear_acceleration_y = []
        self.linear_acceleration_z = []
        self.linear_acceleration_covariance = []
        self.topic = ["/sensors/odometry/imu"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t)
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.orientation_x.append(msg.orientation.x)
            self.orientation_y.append(msg.orientation.y)
            self.orientation_z.append(msg.orientation.z)
            self.orientation_w.append(msg.orientation.w)
            self.orientation_covariance.append(msg.orientation_covariance)
            self.angular_velocity_x.append(msg.angular_velocity.x)
            self.angular_velocity_y.append(msg.angular_velocity.y)
            self.angular_velocity_z.append(msg.angular_velocity.z)
            self.angular_velocity_covariance.append(msg.angular_velocity_covariance)
            self.linear_acceleration_x.append(msg.linear_acceleration.x)
            self.linear_acceleration_y.append(msg.linear_acceleration.y)
            self.linear_acceleration_z.append(msg.linear_acceleration.z)
            self.linear_acceleration_covariance.append(msg.linear_acceleration_covariance)
    def writeCSV(self, prefix):
        print "Writing IMU data to file"
        with open('{}_imu_data.csv'.format(prefix), 'w+') as f:
            f.write("%time, orientation_x, orientation_y, orientation_z, orientation_w, orientation_covariance_0, orientation_covariance_1,orientation_covariance_2, orientation_covariance_3, orientation_covariance_4, orientation_covariance_5, orientation_covariance_6, orientation_covariance_7, orientation_covariance_8, angular_velocity_x, angular_velocity_y, angular_velocity_z, angular_velocity_covariance_0, angular_velocity_covariance_1, angular_velocity_covariance_2, angular_velocity_covariance_3, angular_velocity_covariance_4, angular_velocity_covariance_5,angular_velocity_covariance_6, angular_velocity_covariance_7, angular_velocity_covariance_8, linear_acceleration_x, linear_acceleration_y, linear_acceleration_z, linear_acceleration_covariance_0, linear_acceleration_covariance_1, linear_acceleration_covariance_2, linear_acceleration_covariance_3, linear_acceleration_covariance_4, linear_acceleration_covariance_5,linear_acceleration_covariance_6, linear_acceleration_covariance_7, linear_acceleration_covariance_8\n")
            for k in range(len(self.t_stamp)):
                f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(self.t_stamp[k], self.orientation_x[k], self.orientation_y[k], self.orientation_z[k], self.orientation_w[k], self.orientation_covariance[k], self.angular_velocity_x[k], self.angular_velocity_y[k], self.angular_velocity_z[k], self.angular_velocity_covariance[k], self.linear_acceleration_x[k], self.linear_acceleration_y[k], self.linear_acceleration_z[k], self.linear_acceleration_covariance[k]))

class VelocityCommandPlotter:
    def __init__(self):
        self.vx = []
        self.vy = []
        self.vz = []
        self.omega_x = []
        self.omega_y = []
        self.omega_z = []
        self.t = []
        self.topic = ["/sensors/odometry/velocity/cmd"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.vx.append(msg.linear.x)
            self.vy.append(msg.linear.y)
            self.vz.append(msg.linear.z)
            self.omega_x.append(msg.angular.x)
            self.omega_y.append(msg.angular.y)
            self.omega_z.append(msg.angular.z)
           
    def writeCSV(self, prefix):
        print "Writing Velocity Command to file"
        with open('{}_velocity_cmd.csv'.format(prefix), 'w+') as f:
            f.write("%time, linear_velocity_x, linear_velocity_y, linear_velocity_z, angular_velocity_x, angular_velocity_y, angular_velocity_z\n")
            for k in range(len(self.t)):
                f.write("{}, {}, {}, {}, {}, {}, {}\n".format(self.t[k], self.vx[k], self.vy[k], self.vz[k], self.omega_x[k], self.omega_y[k], self.omega_z[k]))

class PosePlotter:
    def __init__(self):
        self.pose_x = []
        self.pose_y = []
        self.pose_z = []
        self.orientation_x = []
        self.orientation_y = []
        self.orientation_z = []
        self.orientation_w = []
        self.twist_x = []
        self.twist_y = []
        self.twist_z = []
        self.twist_angular_x = []
        self.twist_angular_y = []
        self.twist_angular_z = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/pose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.pose_x.append(msg.pose.pose.position.x)
            self.pose_y.append(msg.pose.pose.position.y)
            self.pose_z.append(msg.pose.pose.position.z)
            self.orientation_x.append(msg.pose.pose.orientation.x)
            self.orientation_y.append(msg.pose.pose.orientation.y)
            self.orientation_z.append(msg.pose.pose.orientation.z)
            self.orientation_w.append(msg.pose.pose.orientation.w)
            self.twist_x.append(msg.twist.twist.linear.x)
            self.twist_y.append(msg.twist.twist.linear.y)
            self.twist_z.append(msg.twist.twist.linear.z)
            self.twist_angular_x.append(msg.twist.twist.angular.x)
            self.twist_angular_y.append(msg.twist.twist.angular.y)
            self.twist_angular_z.append(msg.twist.twist.angular.z)
    def writeCSV(self, prefix):
        print "Writing Pose Data to file"
        with open('{}_pose.csv'.format(prefix), 'w+') as f:
            f.write("%time, pose_x, pose_y, pose_z, orientation_x, orientation_y, orientation_z, orientation_w, twist_linear_x, twist_linear_y, twist_linear)z, twist_angular_x, twist_angular_y, twist_angular_z\n")
            for k in range(len(self.t_stamp)):
                f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(self.t_stamp[k], self.pose_x[k], self.pose_y[k], self.pose_z[k], self.orientation_x[k], self.orientation_y[k], self.orientation_z[k], self.orientation_w[k], self.twist_x[k], self.twist_y[k], self.twist_z[k], self.twist_angular_x[k], self.twist_angular_y[k], self.twist_angular_z[k]))



class BagCsvWriter:
    def __init__(self):
        # Create some csv writers
        self.writers = []
        self.writers.append(WheelRotationWriter())
        self.writers.append(AmclPoseWriter())
        self.writers.append(IMUWriter())
        self.writers.append(VelocityCommandPlotter())
        self.writers.append(PosePlotter())

    def run(self, bag_name):
        print "Parsing data from bag " + bag_name
        # Get the list of topics
        topics_to_write = []
        for writer in self.writers:
            topics_to_write.extend(writer.get_topics())
        # Open the bag and parse all of the messages
        with rosbag.Bag(bag_name, 'r') as bag:
            for topic, msg, t in bag.read_messages(topics=topics_to_write):
                for writer in self.writers:
                    writer.parse(topic, msg, t)

        # Let the bag close and write the data now
        print "Writing csv files"
        for writer in self.writers:
            try:
                writer.writeCSV(bag_name.rstrip('.bag'))
            except AttributeError:
                print "Caught error"


        print "Done"

if __name__ == '__main__':
    bag_name = "test.bag"
    if len(sys.argv) < 2:
        print "No bag name supplied.  Trying " + bag_name
    else:
        bag_name = sys.argv[1]
    bp = BagCsvWriter()
    bp.run(bag_name)
    print "Done plotting"