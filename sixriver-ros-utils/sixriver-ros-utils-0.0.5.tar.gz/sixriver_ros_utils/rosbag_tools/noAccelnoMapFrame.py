import rosbag
import sys
#verify correct input arguments: 1 or 2

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		bar_length  - Optional  : character length of bar (Int)
	"""
	str_format = "{0:." + str(decimals) + "f}"
	percents = str_format.format(100 * (iteration / float(total)))
	filled_length = int(round(bar_length * iteration / float(total)))
	bar = ' ' * filled_length + '-' * (bar_length - filled_length)

	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

	if iteration == total:
		sys.stdout.write('\n')
	sys.stdout.flush()



def main(bagName):
	bagFile = bagName
	print "reading: " + str(bagFile)

	oldbag = rosbag.Bag(bagFile)
	bagName = oldbag.filename
	newBagName = bagName + "-noAccelnoMap.bag"

	total = oldbag.get_message_count()

	prevImuTime = None
	print_progress(0, total, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
	with rosbag.Bag(newBagName, 'w') as outbag:
		num = 0
		for topic, msg, t in oldbag.read_messages():
			num = num + 1
			if topic == "/sensors/odometry/imu":
				msg2 = msg
				msg2.linear_acceleration.x = 0;
				msg2.linear_acceleration.y = 0;
				msg2.linear_acceleration.z = 1;
				outbag.write(topic, msg2, t)

			if topic == "/tf":
				shouldWrite = True
				for i in range(len(msg.transforms)):
					if msg.transforms[i].child_frame_id == "odom":
						shouldWrite = False
				if(shouldWrite):
					outbag.write(topic, msg, t)
			else:
				outbag.write(topic, msg, t)
			if(num%1000 == 0):
				print_progress(num, total, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print "invalid number of arguments:   " + str(len(sys.argv))
		print "should be 2: 'bag2csv.py' and 'bagName'"
		sys.exit(1)
	else:
		main(sys.argv[1])