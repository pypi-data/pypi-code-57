#!/usr/bin/env python

# Ping-DPT
# Nicholas Nothom
# 2020

from brping import Ping1D
import pynmea2
import time
import argparse
import os

from builtins import input

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
parser.add_argument('--logdir', action="store", required=False, type=str, default="logs", help="DPT Log Directory. E.g: logs/ ")

args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)

# Make a new Ping
myPing = Ping1D()
if args.device is not None:
    myPing.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    myPing.connect_udp(host, int(port))

if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

if os.path.isdir(args.logdir) is False:
    try:
        os.makedirs(args.logdir)
    except:
        print("Failed to create log directory")

# Create Logging File
logfile_path = args.logdir + "/ping-dpt-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".log"
logfile = open(logfile_path, 'w')
logfile.close()

print("------------------------------------")
print("Starting Ping..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

while True:
    data = myPing.get_distance()

    if data:
        # Prepare Values
        depth_meters = ("{:.3f}".format(data['distance'] * 0.001))
        offset_meters = '0.0'

        # Construct NMEA Sentence
        nmea_sentence = pynmea2.DPT('IN', 'DPT', (depth_meters, offset_meters))
        print(str(nmea_sentence))

        # Write sentence to log
        logfile = open(logfile_path, 'a')
        logfile.writelines(str(nmea_sentence) + '\r')
        logfile.close()
    else:
        print("Failed to get distance data")
    time.sleep(0.1)
