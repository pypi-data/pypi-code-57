#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
from plotters.plot_utils import PlotUtils, ConversionUtils
from plotters.ce_optitrack_test_plotter import CEStopOptitrackTestPlotter
from plotters.ce_test_plotter import CEStopTestPlotter
from plotters.docking_plotter import DockingPlotter
import rosbag

class BagPlotter:
    def __init__(self, marker_name):
        # Create some plotters
        self.plotters = []
        #self.plotters.append(VelocityPlotter())
        #self.plotters.append(RPMPlotter())
        #self.plotters.append(CEStopTestPlotter())
        #self.plotters.append(CEStopOptitrackTestPlotter(marker_name))
        self.plotters.append(DockingPlotter())
        self.types = {}

    def run(self, bag_name):
        print "Parsing data from bag " + bag_name
        # Get the list of topics
        topics_to_plot = []
        for plotter in self.plotters:
            topics_to_plot.extend(plotter.get_topics())
        # Open the bag and parse all of the messages
        with rosbag.Bag(bag_name, 'r') as bag:
            print "Topics: {}".format(topics_to_plot)
            for topic, msg, t in bag.read_messages():
                # print "Topic: {}".format(topic)
                if not msg._type in self.types:
                    self.types[msg._type] = msg._full_text
                for plotter in self.plotters:
                    plotter.parse(topic, msg, t)
        # Let the bag close and plot the data now

        print "Plotting the data now"
        fignum = 0
        for plotter in self.plotters:
            fignum = plotter.plot(fignum)
            with open(bag_name + "_res.txt", 'w') as file:
                try:
                    plotter.writeFile(file)
                except AttributeError:
                    continue
            with open(bag_name + "_csv.csv", 'w') as file:
                try:
                    plotter.writeCsv(file)
                except AttributeError:
                    continue
        plt.show()

if __name__ == '__main__':
    bag_name = "/home/dan/sample.bag"
    if len(sys.argv) < 2:
        print "No bag name supplied.  Trying " + bag_name
    else:
        bag_name = sys.argv[1]
    if len(sys.argv) > 2:
        bp = BagPlotter(sys.argv[2])
    else:
        bp = BagPlotter("")
    bp.run(bag_name)
    print "Done plotting"
