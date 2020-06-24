#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cmx
import matplotlib.colors as mpl_colors
from matplotlib.lines import Line2D
from tf.transformations import euler_from_quaternion
import numpy as np
import rosbag
import re

class PlotUtils:
    @staticmethod
    def getColorMap(num_colors):
        '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
        RGB color.'''
        color_norm  = mpl_colors.Normalize(vmin=0, vmax=num_colors)
        scalar_map = mpl_cmx.ScalarMappable(norm=color_norm, cmap='hsv')
        def map_index_to_rgb_color(index):
            return scalar_map.to_rgba(index)
        return map_index_to_rgb_color
    @staticmethod
    def getMarkerStyle(num):
        markers = []
        for m in Line2D.markers:
            try:
                if len(m) == 1 and m != ' ':
                    markers.append(m)
            except TypeError:
                pass

        styles = markers + [
            r'$\lambda$',
            r'$\bowtie$',
            r'$\circlearrowleft$',
            r'$\clubsuit$',
            r'$\checkmark$']

        return styles[num % len(styles)]
    @staticmethod
    def getLineStyle(num):
        linestyles = ['-', '--', ':']
        return linestyles[num % len(linestyles)]
    @staticmethod
    def runningMean(x, num_samples):
        return np.convolve(x, np.ones((num_samples,))/num_samples)[(num_samples - 1):]

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

class HeaderDeltaTPlotter:
    class DataStruct:
        def __init__(self):
            self.t = []
            self.dt = []
            self.t_bag = []
            self.dt_bag = []
        def add(self, tval, bagval):
            if len(self.t) == 0:
                self.dt.append(0)
                self.dt_bag.append(0)
            else:
                self.dt.append(tval - self.t[-1])
                self.dt_bag.append(bagval - self.t_bag[-1])
            self.t.append(tval)
            self.t_bag.append(bagval)

    def __init__(self):
        self.data = {}
        self.topics = ["/sensors/lidar/scan/raw",
                        "/sensors/lidar/scan/filtered",
                        "/sensors/odometry/pose",
                        "/sensors/odometry/rpm/raw"]
    def get_topics(self):
        return self.topics
    def parse(self, topic, msg, t):
        if (topic in self.topics):
            key = topic
            if key not in self.data:
                self.data[key] = HeaderDeltaTPlotter.DataStruct()
            self.data[key].add(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9, t.to_sec())

    def plot(self, fignum, ax=None):
        # Check for data before trying to plot
        if not self.data:
            print "No delta t data to plot"
            return fignum

        # Get all of the keys in a list (to preserve order)
        keys = self.data.keys()
        cmap = PlotUtils.getColorMap(len(keys))

        plt.figure(fignum)
        ax1 = plt.subplot(111)
        legendCore = []
        num = 0
        for key in keys:
            ax1.plot(self.data[key].t, self.data[key].dt, '-*', color=cmap(num))
            legendCore += [key]
            num += 1
        plt.title("Stamped sample dt")
        plt.xlabel("Time (s)")
        plt.ylabel("Sample dt (s)")
        plt.legend(legendCore)
        fignum += 1
    def writeCSV(self, fp):
        # output data as a csv
        fp.write("Timing data\n")
        for key in self.data.keys():
            fp.write(key + " - t (bagged), t (stamp), dt (bagged), dt (stamp)\n")
            data = self.data[key]
            for k in range(len(data.t)):
                fp.write("{}, {}, {}, {}\n".format(data.t[k], data.t_bag[k], data.dt[k], data.dt_bag[k]))

class HostCPUDataPlotter:
    class DataStruct:
        def __init__(self, ncores):
            self.t = []
            self.cores = ncores
            self.cpu_load_mean = [[] for i in range(ncores)]
            self.cpu_load_std = [[] for i in range(ncores)]
            self.cpu_load_max = [[] for i in range(ncores)]
            self.phymem_used_mean = []
            self.phymem_used_std = []
            self.phymem_used_max = []
            self.phymem_avail_mean = []
            self.phymem_avail_std = []
            self.phymem_avail_max = []

    def __init__(self):
        self.data = {}
        self.topic = ["/host_statistics"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            key = msg.hostname
            if key not in self.data:
                self.data[key] = HostCPUDataPlotter.DataStruct(len(msg.cpu_load_mean))

            if (len(msg.cpu_load_mean) != self.data[key].cores):
                print "Received new host cpu data message with incorrect number of cores.  Expected: %d, got: %d".format(self.data[key].cores, len(msg.cpu_load_mean))
            self.data[key].t += [(msg.window_start.to_sec() + msg.window_stop.to_sec()) / 2]
            for k in range(self.data[key].cores):
                self.data[key].cpu_load_mean[k] += 1 * [msg.cpu_load_mean[k]]
                self.data[key].cpu_load_max[k] += 1 * [msg.cpu_load_max[k]]
                self.data[key].cpu_load_std[k] += 1 * [msg.cpu_load_std[k]]

            self.data[key].phymem_used_mean += 1 * [msg.phymem_used_mean]
            self.data[key].phymem_used_std += 1 * [msg.phymem_used_std]
            self.data[key].phymem_used_max += 1 * [msg.phymem_used_max]
            self.data[key].phymem_avail_mean += 1 * [msg.phymem_avail_mean]
            self.data[key].phymem_avail_std += 1 * [msg.phymem_avail_std]
            self.data[key].phymem_avail_max += 1 * [msg.phymem_avail_max]

    def plot(self, fignum, ax=None):
        # Check for data before trying to plot
        if not self.data:
            print "No cpu host data to plot"
            return fignum

        # Get all of the keys in a list (to preserve order)
        keys = self.data.keys()
        cmapMem = PlotUtils.getColorMap(len(keys) * 2)

        ncores = 0
        for key in keys:
            ncores += self.data[key].cores
        cmapCores = PlotUtils.getColorMap(ncores)

        # Plot the data
        ## CPU Load
        plt.figure(fignum)
        ax1 = plt.subplot(111)
        legendCore = []
        corenum = 0
        for key in keys:
            for j in range(self.data[key].cores):
                ax1.plot(self.data[key].t, self.data[key].cpu_load_mean[j], '-*', color=cmapCores(corenum))
                corenum += 1
                legendCore += [key + "-" + str(j)]
        plt.title("Mean CPU load")
        plt.xlabel("Time (s)")
        plt.ylabel("Load (%)")
        plt.legend(legendCore)
        fignum += 1

        # plt.figure(fignum)
        # ax1 = plt.subplot(111)
        # legendMem = []
        # for key, k in zip(keys, range(len(keys))):
        #     ax1.plot(self.data[key].t, self.data[key].phymem_used_mean, '-*', color=cmapMem(2 * k))
        #     legendMem += [key + "-Used"]
        #     ax1.plot(self.data[key].t, self.data[key].phymem_avail_mean, '-*', color=cmapMem(2 * k + 1))
        #     legendMem += [key + "-Avail"]
        # plt.title("Max memory load")
        # plt.xlabel("Time (s)")
        # plt.ylabel("Memory (%)")
        # plt.legend(legendMem)
        # fignum += 1

        return fignum

class NodeCPUDataPlotter:
    class DataStruct:
        def __init__(self):
            self.t = []
            self.threads = []
            self.cpu_load_mean = []
            self.cpu_load_std = []
            self.cpu_load_max = []
            self.virt_mem_mean = []
            self.virt_mem_max = []
            self.virt_mem_std = []
            self.real_mem_mean = []
            self.real_mem_max = []
            self.real_mem_std = []

    def __init__(self):
        self.data = {}
        self.topic = ["/node_statistics"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            key = msg.node
            if key not in self.data:
                self.data[key] = NodeCPUDataPlotter.DataStruct()
            self.data[key].t += [(msg.window_start.to_sec() + msg.window_stop.to_sec()) / 2]
            self.data[key].threads += 1 * [msg.threads]
            self.data[key].cpu_load_mean += 1 * [msg.cpu_load_mean]
            self.data[key].cpu_load_std += 1 * [msg.cpu_load_std]
            self.data[key].cpu_load_max += 1 * [msg.cpu_load_max]
            self.data[key].virt_mem_mean += 1 * [msg.virt_mem_mean]
            self.data[key].virt_mem_max += 1 * [msg.virt_mem_max]
            self.data[key].virt_mem_std += 1 * [msg.virt_mem_std]
            self.data[key].real_mem_mean += 1 * [msg.real_mem_mean]
            self.data[key].real_mem_max += 1 * [msg.real_mem_max]
            self.data[key].real_mem_std += 1 * [msg.real_mem_std]

    def plot(self, fignum, ax=None):
        # Check for data before trying to plot
        if not self.data:
            print "No cpu node data to plot"
            return fignum

        # Get all of the keys in a list (to preserve order)
        keys = self.data.keys()
        cmap = PlotUtils.getColorMap(len(keys))

        # Plot the data
        ## CPU Load
        plt.figure(fignum)
        ax1 = plt.subplot(111)
        for key, k in zip(keys, range(len(keys))):
            ax1.plot(self.data[key].t, self.data[key].cpu_load_mean,
                linestyle=PlotUtils.getLineStyle(k), marker=PlotUtils.getMarkerStyle(k),
                color=cmap(k))
        plt.title("Mean CPU load")
        plt.xlabel("Time (s)")
        plt.ylabel("Mean load (%)")
        plt.legend(keys)
        fignum += 1

        ## Memory
        plt.figure(fignum)
        ax = plt.subplot(211)
        for key, k in zip(keys, range(len(keys))):
            ax.plot(self.data[key].t, self.data[key].real_mem_max,
                linestyle=PlotUtils.getLineStyle(k), marker=PlotUtils.getMarkerStyle(k),
                color=cmap(k))
        plt.title("Max real memory")
        plt.xlabel("Time (s)")
        plt.ylabel("Memory")
        plt.legend(keys)

        ax = plt.subplot(212)
        for key, k in zip(keys, range(len(keys))):
            ax.plot(self.data[key].t, self.data[key].virt_mem_max,
                linestyle=PlotUtils.getLineStyle(k), marker=PlotUtils.getMarkerStyle(k),
                color=cmap(k))
        plt.title("Max virtual memory")
        plt.xlabel("Time (s)")
        plt.ylabel("memory")
        plt.legend(keys)
        fignum += 1

        return fignum


class TimingDataPlotter:
    class SamplesStruct:
        def __init__(self):
            self.times = []
            self.durations = []
    class MsgStruct:
        def __init__(self):
            self.times = []
            self.maxes = []
            self.means = []

    def __init__(self):
        self.samples = {}
        self.msgs = {}
        self.topic = ["/monitoring/timing_data"]
        keys_to_skip = ['SSSP-preparingCritics', 'DWAPlannerROS-findBest', 'Reflexes-Loop',
            'SSSP-scoring trajectories', 'DWAPlannerROS-PlanCall', 'DWAPlannerROS-dwaComputeVelCommands',
            'MoveBase-ControllerLoop', 'MoveBase-ControllerExecution', 'AMCL-LaserCB',
            'DWAPlannerROS-UpdatePlanCosts', '^map', 'global_costmap']

        self.keys_to_skip = []
        for key in keys_to_skip:
            self.keys_to_skip.append(re.compile(key))

        #self.keys_to_skip=[]
    def exclude_key(self, key):
        for reg in self.keys_to_skip:
            if reg.match(key):
                return True
        return False

    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            key = msg.id
            if self.exclude_key(key):
                return
            # process the data
            durations = []
            times = []
            maxVal = 0
            meanVal = 0
            for s in msg.samples:
                durations.append(s.duration)
                times.append(s.sample_end_time.to_sec())
                if (s.duration > maxVal):
                    maxVal = s.duration
                meanVal += s.duration
            if len(msg.samples) > 0:
                meanVal /= len(msg.samples)
            else:
                meanVal = 0;

            # Acutally put them in
            if key not in self.samples:
                self.samples[key] = TimingDataPlotter.SamplesStruct()
            self.samples[key].times.extend(times)
            self.samples[key].durations.extend(durations)

            # Add the main samples
            if key not in self.msgs:
                self.msgs[key] = TimingDataPlotter.MsgStruct()
            self.msgs[key].times.append(msg.end_time.to_sec())
            self.msgs[key].maxes.append(maxVal)
            self.msgs[key].means.append(meanVal)

    def plot(self, fignum):
        # Check for data before trying to plot
        if not self.samples:
            print "No timing data to plot"
            return fignum

        num_samples = len(self.samples)
        cm = PlotUtils.getColorMap(num_samples)

        # Plot the data
        plt.figure(fignum)
        ax1 = plt.subplot(111)
        legend = []
        kk = 0
        for key, val in self.samples.iteritems():
            ax1.plot(val.times, val.durations, color=cm(kk), marker=PlotUtils.getMarkerStyle(kk), linestyle=PlotUtils.getLineStyle(kk))
            legend.append(key)
            kk += 1
        plt.title("Timing data over time")
        plt.xlabel("Time (s)")
        plt.ylabel("Duration (ms)")

        plt.legend(legend)

        fignum += 1
        plt.figure(fignum)
        ax2 = plt.subplot(111)
        legend2 = []
        histos = []
        for key, val in self.samples.iteritems():
            histos.append(val.durations)
            legend2.append(key)

        bin_list = np.logspace(-3, 1, 40)
        ax2.hist(histos, bins=bin_list, normed=True, histtype='step')
        plt.gca().set_xscale("log")
        plt.title("Normalized timing histogram")
        plt.xlabel("Duration (ms)")
        plt.ylabel("Normalized count")
        plt.legend(legend2)
        return fignum + 1

class RPMCommandPlotter:
    def __init__(self):
        self.left = []
        self.right = []
        self.t = []
        self.topic = ["/sensors/odometry/rpm/cmd"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.left.append(msg.left_wheel_rpm)
            self.right.append(msg.right_wheel_rpm)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.left, 'k-*')
        plt.setp(ax1.get_xticklabels(), visible=False)
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.right, 'k-*')
        return fignum + 1

class RPMFeedbackPlotter:
    def __init__(self):
        self.left = []
        self.right = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/rpm/raw"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.left.append(msg.left_wheel_rpm)
            self.right.append(msg.right_wheel_rpm)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.left, 'k-*')
        plt.setp(ax1.get_xticklabels(), visible=False)
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.right, 'k-*')
        return fignum + 1
    def writeCSV(self, fh):
        print "Writing to file"
        fh.write("RPM Feedback\n")
        fh.write("t (bagged), t (stamp), left, right\n")
        for k in range(len(self.t)):
            fh.write("{}, {}, {}, {}\n".format(self.t[k], self.t_stamp[k], self.left[k], self.right[k]))

class RPMPlotter:
    def __init__(self):
        self.commandPlt = RPMCommandPlotter()
        self.feedbackPlt = RPMFeedbackPlotter()
        self.topics = []
        self.topics.extend(self.commandPlt.get_topics())
        self.topics.extend(self.feedbackPlt.get_topics())
    def get_topics(self):
        return self.topics
    def parse(self, topic, msg, t):
        if (topic in self.topics):
            self.commandPlt.parse(topic, msg, t)
            self.feedbackPlt.parse(topic, msg, t)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        plt.plot(self.commandPlt.t, self.commandPlt.left, 'k-*',
            self.feedbackPlt.t, self.feedbackPlt.left, 'b-o',
            self.commandPlt.t, self.commandPlt.right, 'r-*',
            self.feedbackPlt.t, self.feedbackPlt.right, 'g-o')
        plt.ylabel('Wheel speed (rpm)')
        plt.xlabel('Time (s)')

        plt.legend(['Left Command', 'Left Response', 'Right Command', 'Right Response'])
        plt.title("Velocity command and response")
        return fignum + 1
    def writeCSV(self, fp):
        self.feedbackPlt.writeCSV(fp)

class WheelRotationPlotter:
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
            scale = 4096 * 10
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.leftCnt.append(msg.leftWheelAbsRotationCount * scale)
            self.rightCnt.append(msg.leftWheelAbsRotationCount * scale)
            if (len(self.leftCnt) > 1):
                leftSpd = (self.leftCnt[-1] - self.leftCnt[-2]) #/ (self.t_stamp[-1] - self.t_stamp[-2])
                self.leftSpd.append(leftSpd)
            else:
                self.leftSpd.append(0)
            if (len(self.rightCnt) > 1):
                rightSpd = (self.rightCnt[-1] - self.rightCnt[-2]) #/ (self.t_stamp[-1] - self.t_stamp[-2])
                if rightSpd > 0.001:
                    print "-1: {}, -2: {}, spd: {}".format(self.rightCnt[-1], self.rightCnt[-2], rightSpd)
                self.rightSpd.append(rightSpd)
            else:
                self.rightSpd.append(0)           
    def plot(self, fignum):
        # Plot the encoder data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t_stamp, self.leftCnt, 'k-*',
            self.t_stamp, self.rightCnt, 'r-o')
        plt.ylabel('Wheel cnt (absolute)')
        plt.legend(['Left', 'Right'])
        plt.title("Wheel encoder counts")
        # Plot wheel velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t_stamp, self.leftSpd, 'k-*')
        #    self.t_stamp, self.rightSpd, 'r-o')
        plt.xlabel('Time (s)')
        plt.ylabel('Wheel vel estimate (cnt/s)')
        return fignum + 1
    def writeCSV(self, fh):
        pass

class VelocityCommandPlotter:
    def __init__(self):
        self.v = []
        self.omega = []
        self.t = []
        self.a = []
        self.topic = ["/sensors/odometry/velocity/cmd"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.v.append(msg.linear.x)
            self.omega.append(msg.angular.z)
            if (len(self.v) > 1):
                self.a.append( (self.v[-1] - self.v[-2]) / (self.t[-1] - self.t[-2]))
            else:
                self.a.append(0)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')
        return fignum + 1

class VelocityFeedbackPlotter:
    def __init__(self):
        self.v = []
        self.omega = []
        self.a = []
        self.t = []
        self.t_stamp = []
        self.v_total = 0
        self.v_cnt = 0
        self.topic = ["/sensors/odometry/pose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.v.append(msg.twist.twist.linear.x)
            self.omega.append(msg.twist.twist.angular.z)
            if (self.v[-1] > 0):
                self.v_total += self.v[-1]
                self.v_cnt += 1
            if (len(self.v) > 1):
                a = (self.v[-1] - self.v[-2]) / (self.t_stamp[-1] - self.t_stamp[-2])
                self.a.append(a)
            else:
                self.a.append(0)

    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')

        return fignum + 1

class VelocityEstimatePlotter:
    def __init__(self):
        self.v = []
        self.omega = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/velocity/estimate"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.v.append(msg.twist.twist.linear.x)
            self.omega.append(msg.twist.twist.angular.z)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')
        return fignum + 1

class VelocityFromPosePlotter:
    def __init__(self):
        self.x = []
        self.y = []
        self.theta = []
        self.v = []
        self.omega = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/pose"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.x.append(msg.pose.pose.position.x)
            self.y.append(msg.pose.pose.position.y)
            self.theta.append(ConversionUtils.quat2Yaw(msg.pose.pose.orientation))

            if (len(self.x) > 1 and len(self.y) > 1):
                dx = self.x[-1] - self.x[-2]
                dy = self.y[-1] - self.y[-2]
                v = np.sqrt(dx * dx + dy * dy) / (self.t_stamp[-1] - self.t_stamp[-2])
                self.v.append(v)
            else:
                self.v.append(0)
            
            if (len(self.theta) > 1):
                w = ConversionUtils.clampAngle(self.theta[-1] - self.theta[-2]) / (self.t_stamp[-1] - self.t_stamp[-2])
                self.omega.append(w)
            else:
                self.omega.append(0)

    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')
        return fignum + 1

class VelocityEstimatePlotter:
    def __init__(self):
        self.v = []
        self.omega = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/odometry/velocity/estimate"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.v.append(msg.twist.twist.linear.x)
            self.omega.append(msg.twist.twist.angular.z)
    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')
        return fignum + 1

class DistanceFromWallPlotter:
    def __init__(self):
        self.dist = []
        self.v = []
        self.t = []
        self.t_stamp = []
        self.topic = ["/sensors/lidar/scan"]
        self.half_angle = 0.05
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.dist.append(self.getDistance(msg))

            if len(self.dist) > 1:
                dx = self.dist[-1] - self.dist[-2]
                v = -dx / (self.t_stamp[-1] - self.t_stamp[-2])
                self.v.append(v)
            else:
                self.v.append(0)

    def getDistance(self, scan):
        # Calculate distance to wall
        dist = -1
        for k in range(len(scan.ranges)):
            angle = k * scan.angle_increment + scan.angle_min
            if angle >= -self.half_angle and angle < self.half_angle:
                ray_range = scan.ranges[k]
                if ray_range < scan.range_min or ray_range > scan.range_max:
                    continue
                if dist < 0 or ray_range < dist:
                    dist = ray_range
        return dist

    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(211)
        plt.plot(self.t, self.v, 'k-*')
        # Plot angular velocity data
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot(self.t, self.omega, 'k-*')
        return fignum + 1

class VelocityPlotter:
    def __init__(self):
        self.commandPlt = VelocityCommandPlotter()
        self.feedbackPlt = VelocityFeedbackPlotter()
        self.estimatePlt = VelocityFromPosePlotter()
        self.distPlt = DistanceFromWallPlotter()
        self.topics = []
        self.topics.extend(self.commandPlt.get_topics())
        self.topics.extend(self.feedbackPlt.get_topics())
        self.topics.extend(self.estimatePlt.get_topics())
        self.topics.extend(self.distPlt.get_topics())

    def get_topics(self):
        return self.topics
    def parse(self, topic, msg, t):
        if (topic in self.topics):
            self.commandPlt.parse(topic, msg, t)
            self.feedbackPlt.parse(topic, msg, t)
            self.estimatePlt.parse(topic, msg, t)
            self.distPlt.parse(topic, msg, t)

    def plot(self, fignum):
        # Plot the velocity data on a subplot with shared x axes
        plt.figure(fignum)
        ax1 = plt.subplot(311)
        plt.plot(self.commandPlt.t, self.commandPlt.v, 'k-*',
            self.feedbackPlt.t_stamp, self.feedbackPlt.v, 'b-o'
            )
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Command', 'Response', 'Estimate'])
        plt.title("Velocity command and response")
        # Plot angular velocity data
        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot(self.commandPlt.t, self.commandPlt.omega, 'k-*',
            self.feedbackPlt.t_stamp, self.feedbackPlt.omega, 'b-o'
            )
        plt.xlabel('Time (s)')
        plt.ylabel('Angular velocity (rad/s)')

        # Plot distance from wall
        ax3 = plt.subplot(313, sharex=ax1)
        plt.plot(self.distPlt.t_stamp, self.distPlt.dist, 'k-*')
        plt.xlabel('Time (s)')
        plt.ylabel('Distance from wall [m]')
        #plt.legend(['distance'])

        # ax3 = plt.subplot(313, sharex=ax1)
        # plt.plot(self.commandPlt.t, self.commandPlt.a, 'k-*',
        #     self.feedbackPlt.t_stamp, self.feedbackPlt.a, 'b-o',
        #     self.feedbackPlt.t_stamp, PlotUtils.runningMean(self.feedbackPlt.a, 10), 'r-o')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Linear acceleration (m/s^2)')
        # plt.legend(['Command', '2-Sample Response', '10-Sample Averaged Response'])

        if self.feedbackPlt.v_cnt > 0:
            print "Average velocity: {} over {} samples".format(self.feedbackPlt.v_total / self.feedbackPlt.v_cnt, self.feedbackPlt.v_cnt)

        return fignum + 1

class AmclJumpPlotter:
    def __init__(self):
        self.amcl_x = []
        self.amcl_y = []
        self.amcl_theta = []
        self.odom2map_x = []
        self.odom2map_y = []
        self.odom2map_theta = []
        self.robot2odom_x = []
        self.robot2odom_y = []
        self.robot2odom_theta = []
        self.diff_x = []
        self.diff_y = []
        self.diff_theta = []
        self.diff_lin = []
        self.t_stamp = []
        self.topic = ["/localization_adjustment"]
    def get_topics(self):
        return self.topic
    def parse(self, topic, msg, t):
        if (topic == self.topic[0]):
            #self.t.append(t.to_sec())
            self.t_stamp.append(msg.header.stamp.secs + msg.header.stamp.nsecs * 1e-9)
            self.amcl_x.append(msg.poses[0].position.x)
            self.amcl_y.append(msg.poses[0].position.y)
            self.amcl_theta.append(ConversionUtils.quat2Yaw(msg.poses[0].orientation))

            self.odom2map_x.append(msg.poses[1].position.x)
            self.odom2map_y.append(msg.poses[1].position.y)
            self.odom2map_theta.append(ConversionUtils.quat2Yaw(msg.poses[1].orientation))

            self.robot2odom_x.append(msg.poses[2].position.x)
            self.robot2odom_y.append(msg.poses[2].position.y)
            self.robot2odom_theta.append(ConversionUtils.quat2Yaw(msg.poses[2].orientation))

            if (len(self.odom2map_x) >= 2 and
                len(msg.poses) == 3):
                # Calculate the diff
                dx = self.odom2map_x[-1] - self.odom2map_x[-2]
                dy = self.odom2map_y[-1] - self.odom2map_y[-2]
                dtheta = ConversionUtils.clampAngle(self.odom2map_theta[-1] - self.odom2map_theta[-2])
                dlin = np.sqrt(dx * dx + dy * dy)
                self.diff_x.append(dx)
                self.diff_y.append(dy)
                self.diff_theta.append(dtheta)
                self.diff_lin.append(dlin)
            else:
                self.diff_x.append(0)
                self.diff_y.append(0)
                self.diff_theta.append(0)
                self.diff_lin.append(0)

    def plot(self, fignum):
        # Plot some stuff
        plt.figure(fignum)

        plt.plot(self.t_stamp, self.diff_x, 'k-*',
            self.t_stamp, self.diff_y, 'b->',
            self.t_stamp, self.diff_theta, 'r-<')

        plt.xlabel("Time (s)")
        plt.ylabel("Jump")
        plt.legend(["Diff x", "Diff y", "Diff yaw"])
        plt.title("Amcl jumps over time")
        fignum += 1

        plt.figure(fignum)

        linscale = (np.array(self.diff_lin) * 100)**2

        plt.scatter(self.amcl_x, self.amcl_y,
            c=self.diff_lin, cmap=plt.get_cmap("BuGn"),
            s=linscale)
        plt.xlabel("X position (m)")
        plt.ylabel("Y position (m)")
        plt.title("Linear amcl jumps over amcl space")
        plt.colorbar()
        fignum += 1
        #
        plt.figure(fignum)

        angscale = (np.array(self.diff_theta) * 100)**2

        plt.scatter(self.amcl_x, self.amcl_y,
            c=self.diff_theta, cmap=plt.get_cmap("BuGn"),
            s=angscale)
        plt.xlabel("X position (m)")
        plt.ylabel("Y position (m)")
        plt.title("Angular amcl jumps over amcl space")
        plt.colorbar()
        fignum += 1

        plt.figure(fignum)


        plt.scatter(self.robot2odom_x, self.robot2odom_y,
            c=self.diff_lin, cmap=plt.get_cmap("BuGn"),
            s=linscale)
        plt.xlabel("X position (m)")
        plt.ylabel("Y position (m)")
        plt.title("Linear jumps over odom space ")
        plt.colorbar()
        fignum += 1
        #
        plt.figure(fignum)

        plt.scatter(self.robot2odom_x, self.robot2odom_y,
            c=self.diff_theta, cmap=plt.get_cmap("BuGn"),
            s=angscale)
        plt.xlabel("X position (m)")
        plt.ylabel("Y position (m)")
        plt.title("Angular jumps over odom space")
        plt.colorbar()
        fignum += 1


        return fignum


class BagPlotter:
    def __init__(self):
        # Create some plotters
        self.plotters = []
        self.plotters.append(VelocityPlotter())
        self.plotters.append(WheelRotationPlotter())
        #self.plotters.append(RPMPlotter())
        #self.plotters.append(TimingDataPlotter())
        #self.plotters.append(NodeCPUDataPlotter())
        #self.plotters.append(HostCPUDataPlotter())
        #self.plotters.append(HeaderDeltaTPlotter())
        #self.plotters.append(AmclJumpPlotter())

    def run(self, bag_name):
        print "Parsing data from bag " + bag_name
        # Get the list of topics
        topics_to_plot = []
        for plotter in self.plotters:
            topics_to_plot.extend(plotter.get_topics())
        # Open the bag and parse all of the messages
        with rosbag.Bag(bag_name, 'r') as bag:
            with open('bag.txt', 'w') as fp:
                fp.write("{}".format(bag))
            for topic, msg, t in bag.read_messages(topics=topics_to_plot):
                for plotter in self.plotters:
                    plotter.parse(topic, msg, t)
        # Let the bag close and plot the data now
        print "Printing data to file"
        with open("out.txt", 'w') as file:
            for plotter in self.plotters:
                try:
                    plotter.writeCSV(file)
                except AttributeError:
                    continue


        print "Plotting the data now"
        fignum = 0
        for plotter in self.plotters:
            fignum = plotter.plot(fignum)
        plt.show()

if __name__ == '__main__':
    bag_name = "test.bag"
    if len(sys.argv) < 2:
        print "No bag name supplied.  Trying " + bag_name
    else:
        bag_name = sys.argv[1]
    bp = BagPlotter()
    bp.run(bag_name)
    print "Done plotting"
