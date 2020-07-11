#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist 


class UniToDiff():

	def __init__(self):
		rospy.init_node("UniToDiff")
		nodename = rospy.get_name()
		self.base_width = 0.2 
		self.R = 0.1
		self.pub_lmotor = rospy.Publisher('lwheel_vtarget', Float32,queue_size=10)
		self.pub_rmotor = rospy.Publisher('rwheel_vtarget', Float32,queue_size=10)
		rospy.Subscriber('cmd_vel', Twist, self.twistCallback)
		self.rate = 2
		self.left = 0
		self.right = 0
		
	def main_fun(): 
		while not rospy.is_shutdown():
			self.publish_Def()
			self.rate.sleep()
			
	def publish_Def(): 
		self.vl = ( (2.0 * self.dx) - (self.dz*self.base_width) ) / (2.0 * self.R)
		self.vr = ( (2.0 * self.dx) + (self.dz*self.base_width) ) / (2.0 * self.R)
		self.pub_lmotor.publish(vr)
		self.pub_rmotor.publish(vl)

	def uni_call_back( self, data):
		self.dx = data.linear.x
		self.dy = 0
		self.dz = data.angular.z
		

if __name__ == '__main__':
	""" main """
	UniToDiff = UniToDiff()
	UniToDiff.main_fun()