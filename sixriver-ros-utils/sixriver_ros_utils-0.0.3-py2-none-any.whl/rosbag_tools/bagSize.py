#!/usr/bin/env python
# Print total cumulative serialized msg size per topic
#how to use = python bagSize.py <bag_name> <topic to look > <topic2 to look at> <topic3 to look at>
import rosbag
import sys
from texttable import Texttable



def sizeof_fmt(num):
    for letter in ['','K','M','G']:
        if abs(num) < 1024.0:
            return "%3.2f%sB" % (num, letter)
        num /= 1024.0


observed_topics = []
numArgs = len(sys.argv)
for i in range(2, (numArgs)):
  observed_topics.append(sys.argv[i])

topic_size_dict = {}
for topic, msg, time in rosbag.Bag(sys.argv[1], 'r').read_messages(raw=True):
  topic_size_dict[topic] = topic_size_dict.get(topic, 0) + len(msg[1])
topic_size_list = list(topic_size_dict.items())
topic_size_list.sort(key=lambda x: x[1])
totalSize = 0
for topic, size in topic_size_list:
  totalSize = totalSize + size

t = Texttable()
t.add_row(['Topic Name', 'Size', 'Percentage of bag'])
for topic, size in topic_size_list:
  t.add_row([topic, sizeof_fmt(size), "{0:.1%}".format(float(size)/float(totalSize))])
print(t.draw())

print ""
print "Total size of the bag %s" % sizeof_fmt(totalSize)
print ""

t2 = Texttable()
t2.add_row(['Topic Name', 'Size', 'Percentage of bag'])
print observed_topics
for topic, size in topic_size_list:
  for top in observed_topics:
    if top == topic:
      t2.add_row([topic, sizeof_fmt(size), "{0:.1%}".format(float(size)/float(totalSize))])
print(t2.draw())