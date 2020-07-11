#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('tagid', String, queue_size=10)
	rospy.init_node('tagsPublisher', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	pub.publish("notag")
	while not rospy.is_shutdown():
		snedit = input("Do you want to send a tag")
		if sendit == 'y':
			tagid = input("ENter a Tag please")
			rospy.loginfo(tagid)
			pub.publish(tagid)
			rate.sleep()
		else:
			pass

			

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass




