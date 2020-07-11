#!/usr/bin/env python

import rospy
import roslib
from std_msgs.msg import Float32
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist 

from numpy import interp

rospy.init_node("combineMotors")
nodename = rospy.get_name()
rospy.loginfo("%s started" % nodename)
w =  0.125


left = 0
right = 0
speed_data = Int32MultiArray()

def leftCallBack(msg):

	global left 
	left = msg.data

def rightCallBack(msg):

	global right 
	right = msg.data

pub_speed = rospy.Publisher('/set_speed',Int32MultiArray,queue_size=10)
rospy.Subscriber('/right_wheel_speed', Float32,rightCallBack)
rospy.Subscriber('/left_wheel_speed', Float32, leftCallBack)
rate = rospy.get_param("~rate", 50)
r = rospy.Rate(rate)


def publishData(left, right):
	global pub_speed
	right_mapped = int(right)
	left_mapped =  int(left)
	speed_data.data = [right,left]
	pub_speed.publish(speed_data)



if __name__ == '__main__':
	while not rospy.is_shutdown():
		publishData(left, right)
		

