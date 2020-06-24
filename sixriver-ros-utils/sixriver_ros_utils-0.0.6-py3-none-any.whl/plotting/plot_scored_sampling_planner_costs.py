#!/usr/bin/python
import rospy
from base_local_planner.msg import ScoredSamplingPlannerCosts
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import numpy as np
from math import ceil
from matplotlib.colors import LinearSegmentedColormap


class CriticCostPlotter:
    def __init__(self):
        # Do stuff to initialize here
        self.plotted = False
        self.scats = []
        self.axes = []
        self.backgrounds = []
        self.critic_names = ["GP Distance", "Heading", "Oscillation", "Speed Cost", "Velocity",
                             "Obstacle", "Goal front", "Alignment",
                             "Path", "Goal", "Jerk", "Euc dist", "Total Cost"]
        self.cmap = self.generateCMap()

        self.diff_dict = {}

    def callback(self, msg):
        # Receive a new message
        if msg.num_critics + 1 > len(self.critic_names):
            print "Cannot plot due to critic name size mismatch.  Expected {0} critics to plot, but received {1}".format(len(self.critic_names), msg.num_critics + 1)
            return
        if not self.plotted:
            # Only plot the first time until i figure out more
            self.plotted = True
            #print "{}".format(msg)
            #
            print "msg"
            self.plotFirstMessage(msg)
        else:
            pass
            print "more msg at lag {}".format(rospy.Time.now().to_sec() - msg.header.stamp.to_sec())
            self.plotNextMessage(msg)

    def plotFirstMessage(self, msg):

        # Plot a whole message here
        # First, go through the data and convert it into a more plottable form
        #  We want:  v, w, critic_cost[critic_num][cost]
        v, w, costs, picked = self.unwindDataNoOverlap(msg)
        # Printing data
        # Create the plot
        self.fig = plt.figure(0, figsize=(25, 20), dpi=80)
        for k in range (msg.num_critics + 1):
            ax = plt.subplot(2, ceil((msg.num_critics + 1)/2.0), k + 1)
            ax.set_xlim([-0.1, 1.1])
            ax.set_ylim([-1.5, 1.5])
            ax.set_xlabel("v (m/s)")
            ax.set_ylabel("w (rad/s)")
            ax.set_title(self.critic_names[k])
            self.axes.append(ax)
            scat = ax.scatter(v, w, c=costs[k], s=50, cmap=self.cmap, vmin=0.0, vmax=1.0, lw=0)
            self.scats.append(scat)
            # if k == ceil(msg.num_critics/2.0):
            #     self.fig.colorbar(ax)

        scat_final = self.axes[-1].scatter([picked[0]],[picked[1]], c='y', s=75)
        self.scats.append(scat_final)


        # Deal with the differential stuff
        self.addDataToDiffMap(msg)
        v, w, values = self.getPlottableDataFromDiffMap()
        print "Values: {}".format(values)
        self.diff_fig = plt.figure(1, figsize=(25, 20), dpi=80)
        self.diff_axis = plt.subplot(1, 1, 1)
        self.diff_axis.set_xlim([-0.1, 0.1])
        self.diff_axis.set_ylim([-0.3, 0.3])
        self.diff_axis.set_xlabel("v (m/s)")
        self.diff_axis.set_ylabel("w (rad/s)")
        self.diff_axis.set_title("Critic differential histogram");
        self.diff_scat = self.diff_axis.scatter(v, w, c=values, s=15, cmap=self.cmap, lw=0, vmin=0.0, vmax=100.0)

        plt.ion()
        plt.show()
        plt.pause(0.0001)

    def plotNextMessage(self, msg):
        start_t = rospy.Time.now().to_sec()

        # Plot a whole message here
        # First, go through the data and convert it into a more plottable form
        #  We want:  v, w, critic_cost[critic_num][cost]
        v, w, costs, picked = self.unwindDataNoOverlap(msg)
        unwind_t = rospy.Time.now().to_sec()
        # Printing data
        # Create the plot
        # fig = plt.figure(0)
        vw = np.array([v, w], ndmin=2).transpose()
        for k in range (msg.num_critics + 1):
            scat = self.scats[k]
            scat.set_offsets(vw)
            scat.set_array(costs[k])

            ax = self.axes[k]
            #self.fig.canvas.restore_region(self.backgrounds[k])
            ax.draw_artist(ax.patch)
            ax.draw_artist(scat)
            self.fig.canvas.blit(ax.bbox)

        # Take care of the highlighted spot
        scat_final = self.scats[-1]
        scat_final.set_offsets(picked)
        self.axes[-1].draw_artist(scat_final)
        self.fig.canvas.blit(ax.bbox)


        self.addDataToDiffMap(msg)
        v, w, values = self.getPlottableDataFromDiffMap()
        print "Values: {}".format(values)
        print "V: {}, w {}".format(v, w)

        vw = np.array([v, w], ndmin=2).transpose()
        self.diff_scat.set_offsets(vw)
        self.diff_scat.set_array(values)
        self.diff_axis.draw_artist(self.diff_axis.patch)
        self.diff_axis.draw_artist(self.diff_scat)
        self.diff_fig.canvas.blit(self.diff_axis.bbox)

        set_t = rospy.Time.now().to_sec()
        #plt.draw()
        # New draw

        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()
        final_t = rospy.Time.now().to_sec()

        print "Timing: unwind {}, set {}, draw {}, total {}".format(
            unwind_t - start_t, set_t - unwind_t, final_t - set_t, final_t - start_t)

    def unwindData(self, msg):
        num_samples = len(msg.costs)
        v = np.zeros(num_samples)
        w = np.zeros(num_samples)
        costs = [np.zeros(num_samples) for k in range(msg.num_critics + 1)]
        k = 0
        for critic_cost in msg.costs:
            v[k] = critic_cost.v
            w[k] = critic_cost.w
            #v.append(critic_cost.v)
            #w.append(critic_cost.w)
            for kk in range(msg.num_critics):
                costs[kk][k] = critic_cost.costs[kk]
            costs[-1][k] = critic_cost.total_cost
            k += 1

        picked = np.zeros(2)
        picked[0] = msg.selected_v
        picked[1] = msg.selected_w
        return v, w, costs, picked

    def unwindDataNoOverlap(self, msg):
        # We want the cheapest non-negative value for any overlapping points.
        vw_dict = {}
        for critic_cost in msg.costs:
            key = (int(critic_cost.v * 1000), int(critic_cost.w * 1000))
            new_cost = (critic_cost.total_cost, critic_cost.costs)
            if key in vw_dict:
                d_cost = vw_dict[key]
                if new_cost[0] >= 0:
                    if new_cost[0] < d_cost[0] or d_cost[0] < 0:
                        vw_dict[key] = new_cost
            else:
                vw_dict[key] = new_cost


        num_samples = len(vw_dict.keys())
        v = np.zeros(num_samples)
        w = np.zeros(num_samples)
        costs = [np.zeros(num_samples) for k in range(msg.num_critics + 1)]
        k = 0
        for key, value in vw_dict.iteritems():
            v[k] = key[0] / 1000.0
            w[k] = key[1] / 1000.0
            # print "V: {}, W: {}".format(v[k], w[k])

            for kk in range(msg.num_critics):
                costs[kk][k] = value[1][kk]
            costs[-1][k] = value[0]
            k += 1

        picked = np.zeros(2)
        picked[0] = msg.selected_v
        picked[1] = msg.selected_w
        print "Kept {} of {}".format(num_samples, len(msg.costs))
        return v, w, costs, picked

    def addDataToDiffMap(self, msg):
        # Add the data into a dictionary showing steps
        # First, get the middle value
        vmid = msg.start_v
        wmid = msg.start_w

        key = (int((msg.selected_v - vmid) * 1000), int((msg.selected_w - wmid) * 1000))
        if key in self.diff_dict:
            self.diff_dict[key] += 1
        else:
            self.diff_dict[key] = 1


        for critic_cost in msg.costs:
            key = (int((critic_cost.v - vmid) * 1000), int((critic_cost.w - wmid) * 1000))
            if key not in self.diff_dict:
                self.diff_dict[key] = 0

    def getPlottableDataFromDiffMap(self):
        num_samples = len(self.diff_dict.keys())
        v = np.zeros(num_samples)
        w = np.zeros(num_samples)
        values = np.zeros(num_samples)
        k = 0
        for key, value in self.diff_dict.iteritems():
            v[k] = key[0] / 1000.0
            w[k] = key[1] / 1000.0
            # print "V: {}, W: {}".format(v[k], w[k])
            values[k] = value
            k += 1

        return v, w, values

    def generateCMap(self):
        cdict1 = {'red':   ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 1.0, 1.0),
                   (0.001, 0.5, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (0.5, 0.5, 0.5),
                   (1.0, 0.0, 0.0))
        }

        cmap = LinearSegmentedColormap('Custom colors', cdict1)
        cmap.set_under('k')
        cmap.set_over('g')
        return cmap


if __name__ == '__main__':
    # set up the subscriber
    plotter = CriticCostPlotter()
    rospy.init_node('plotter', anonymous=True)
    rospy.Subscriber("/local_planner_costs", ScoredSamplingPlannerCosts, plotter.callback, queue_size=1)
    rospy.spin()