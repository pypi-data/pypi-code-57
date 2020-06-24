import rosbag
import sys
import matplotlib.pyplot as plt
import tf


if (len(sys.argv) != 2):
	print "invalid number of arguments:   " + str(len(sys.argv))
	sys.exit(1)
else:
	bagFile = sys.argv[1]
	print "reading: " + str(bagFile)

oldbag = rosbag.Bag(bagFile)

xs = []
ys = []
thetas = []
ts = []


for topic, msg, t in oldbag.read_messages():
	if topic == "/tf":
		shouldWrite = True
		for i in range(len(msg.transforms)):
			if msg.transforms[i].child_frame_id == "odom":
				quaternion = (
					0,
					0,
					msg.transforms[i].transform.rotation.z,
					msg.transforms[i].transform.rotation.w)
				xs.append(msg.transforms[i].transform.translation.x)
				ys.append(msg.transforms[i].transform.translation.y)
				thetas.append(tf.transformations.euler_from_quaternion(quaternion)[2])
				ts.append(t.to_sec())
plt.figure(0)
plt.plot(ts, thetas, 'k-*')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (rad)')
plt.title('AMCL correction of theta over time while spinning')
plt.show()

