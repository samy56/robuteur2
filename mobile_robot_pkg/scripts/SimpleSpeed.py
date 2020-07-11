#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
rospy.init_node('simple_speed')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
move = Twist()
move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
move.angular.z = 0.0 #Move the with an angular velocity in the z axis

def callback(data):
	tagid = data.data
	move.linear.x = 1.0
	move.angular.z = 0.0
	pub.publish(move)
	if tagid == "0000":
		move.linear.x = 0.5
		move.angular.z = 0.0
		pub.publish(move)
	elif tagid == "1234": 
		move.linear.x = 0.0
		move.angular.z = 0.0
		pub.publish(move)
	


def listener():
	rospy.Subscriber("tagid", String, callback)
	rospy.spin()



if __name__ == '__main__':
	listener()
