#!/usr/bin/python

import sys
import time
import matplotlib.pyplot as plt
from plotters.plot_utils import ConversionUtils
import rosbag
import re


# want: scroll through bag until start event
# record pose at start
# wait until end event
# record pose at end event
# record firmware messages b/t start & end
# record 

# write to output file result csv

# Create separate csv files for all the other topics?

class Pose:
    def __init__(self, msg):
        self.t = msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9
        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        self.z = msg.pose.position.z
        self.theta = ConversionUtils.quat2Yaw(msg.pose.orientation)

class TestResult:
    def __init__(self):
        self.start_msg_set = False
        self.start_time = -100
        self.offset = -100
        self.velocity = -100
        self.curvature = -100
        self.start_pose = None
        self.end_pose = None
        self.firmware_msgs = []
        self.firmware_msg_time = None
        self.poses = []
        self.start_pole = None
        self.end_pole = None


    def toCsv(self):

        firmwareMsgString = '['
        for message in self.firmware_msgs:
            firmwareMsgString += message
            pass
        firmwareMsgString += ']'

        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.start_time,
            self.offset,
            self.velocity,
            self.curvature,
            self.start_pole.x if self.start_pole else "None",
            self.start_pole.y if self.start_pole else "None",
            self.start_pole.z if self.start_pose else "None",
            self.start_pose.x if self.start_pose else "None",
            self.start_pose.y if self.start_pose else "None",
            self.start_pose.theta if self.start_pose else "None",
            self.end_pole.x if self.end_pole else "None",
            self.end_pole.y if self.end_pole else "None",
            self.end_pole.z if self.end_pole else "None",
            self.end_pose.x if self.end_pose else "None",
            self.end_pose.y if self.end_pose else "None",
            self.end_pose.theta if self.end_pose else "None",
            self.firmware_msg_time,
            firmwareMsgString
        )

    def poseToCsv(self):
        longString = ""
        for pose in self.poses:
            longString += "{},{},{},{},".format(pose.x,pose.y,pose.theta,pose.t)
        return longString

    @staticmethod
    def csvHeader():
        return ("start_time, offset, velocity, curvature,"
            " start_pole_x, start_pole_y, start_pole_z,"
            " start_x, start_y, start_theta,"
            " end_pole_x, end_pole_y, end_pole_z,"
            " end_x, end_y, end_theta,"
            " firmware_msg_time,"
            " firmware_msgs,"
            " pose_x, pose_y, pose_theta, pose_time")

class CeTestAnalyzer:
    # Topics used for parsing messages
    START_TOPIC = '/ce_testing/start'
    END_TOPIC = '/ce_testing/end'
    POSE_TOPIC = '/vrpn_client_node/optihat1/mapPose'
    POLE_TOPIC = '/vrpn_client_node/pole/mapPose'
    MSG_TOPIC = '/rosout'

    FIRMWARE_MSG_PREFIX = 'Safety Circuit SysState'

    def __init__(self, file_names):
        self.currentResult = None
        self.pose_list = [None]
        bags = []

        (output_prefix, bags) = self.orderFiles(file_names)
        if len(bags) == 0:
            print "No bag names provided."
            return

        output_name = output_prefix + "_" + str(time.time()) + ".csv"

        with open(output_name, 'w') as fh:
            fh.write("{}\n".format(TestResult.csvHeader()))
            for bag in bags:
                self.runOnBag(bag.strip(), fh)
        
    def orderFiles(self, file_names):

        # File names are in an array. Check that they all have the same prefix, then order them.
        sortableBags = []
        prefix = ''

        for f in file_names:
            split_name = f.split('-ce_test_')
            try:
                val = int(split_name[1][:-4])
            except:
                continue 
            if prefix == '':
                prefix = split_name[0]
            elif prefix != split_name[0]:
                continue
            sortableBags.append((val, f))

        sortableBags = sorted(sortableBags)
        bags = [fn for val, fn in sortableBags]

        return (prefix, bags)

    def writeResult(self, fh):
        print "Writing result"
        fh.write("{},{}\n".format(self.currentResult.toCsv(),self.currentResult.poseToCsv()))

    def handlePoleTopic(self,msg,t):
        #Log pole location
        self.pole = Pose(msg)


    def handlePoseTopic(self, msg, t):
        # print "pose"
        # Log all pose messages into an array.
        if self.pose_list[0] is None:
            self.pose_list = []
        self.pose_list.append(Pose(msg))
        if(self.currentResult != None):
            self.currentResult.poses.append(Pose(msg))

    def handleStartTopic(self, msg, t):
        # print "start"
        if self.currentResult:
            print "Warning: 2 start messages in a row.  Replacing old one"
        self.currentResult = TestResult()
        self.currentResult.offset = msg.z
        self.currentResult.velocity = msg.x
        self.currentResult.curvature = msg.y
        self.currentResult.start_time = t
        self.currentResult.start_pose = self.pose_list[-1]
        self.currentResult.start_pole = self.pole

    def handleEndTopic(self, msg, t, fh):
        # print "end"
        if self.currentResult is None:
            print "Warning:  End message with no start message.  Ignoring"
            return
        self.currentResult.end_pose = self.pose_list[-1]
        self.currentResult.end_pole = self.pole
        self.writeResult(fh)
        self.currentResult = None

    def handleMsgTopic(self, msg, t):
        # Store any messages if there is an active result and it matches
        if self.FIRMWARE_MSG_PREFIX in msg.msg:
            if self.currentResult is None:
                print "Warning: firmware message {} received with no start.  Ignoring.".format(msg.msg)
            else:
                msg.msg = re.sub('\(../src/srs_logic/src/srs_safetyCircuitController.c:97\)', '', msg.msg)
                self.currentResult.firmware_msgs.append(msg.msg)
                self.currentResult.firmware_msg_time = t

    def checkLine(self, topic, msg, t, fh):
        if topic == self.START_TOPIC:
            self.handleStartTopic(msg, t)
        elif topic == self.END_TOPIC:
            self.handleEndTopic(msg, t, fh)
        elif topic == self.POSE_TOPIC:
            self.handlePoseTopic(msg, t)
        elif topic == self.MSG_TOPIC:
            self.handleMsgTopic(msg, t)
        elif topic == self.POLE_TOPIC:
            self.handlePoleTopic(msg, t)

    def runOnBag(self, bag_name, fh):
        print "Parsing data from bag " + bag_name

        # Open the bag and parse all of the messages
        with rosbag.Bag(bag_name, 'r') as bag:
            for topic, msg, t in bag.read_messages():
                self.checkLine(topic, msg, t, fh)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No file name supplied."
    else:
        cta = CeTestAnalyzer(sys.argv[1:])
        print "done"