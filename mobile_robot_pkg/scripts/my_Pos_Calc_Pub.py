#!/usr/bin/env python
import rospy
import math
from math import sin, cos, pi
from geometry_msgs.msg import Pose2D
# from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
# from geometry_msgs.msg import Vector3
# from nav_msgs.msg import Odometry
# import tf
# from tf.broadcaster import TransformBroadcaster
from std_msgs.msg import Int16, Int32, Int64
# from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

rospy.init_node('Pos_Calc_Pub')
left = 0
right= 0
def lwheelCallback(msg):
	global left
	left = msg.data

def rwheelCallback(msg):
	global right
	right = msg.data

c=1

pos_pub = rospy.Publisher("pos", Pose2D, queue_size=10)
rospy.Subscriber("left_ticks", Int32, lwheelCallback)
rospy.Subscriber("right_ticks", Int32, rwheelCallback)

x = 0				  # position in xy plane 
y = 0
th = 0

left = left
right= right

enc_left  = left
enc_right = right
ticks_meter = 10
base_width =0.2
R= 0.1
p= 3.14 	

current_time = rospy.Time.now()
last_time = rospy.Time.now()
r = rospy.Rate(2)
pos = Pose2D()


def publish_Data(x , y, th):
	Pose2D.x = x 
	Pose2D.y =y
	Pose2D.theta=th 
	pos_pub.publish(pos)
	
while not rospy.is_shutdown():
	if c<50:
		current_time = rospy.Time.now()	
		if current_time > last_time:
			
			d_left = float ((2*p*R*(left -  enc_left) )	/  ticks_meter )
			d_right= float ((2*p*R*( right -  enc_right) )  /  ticks_meter)

			# distance traveled is the average of the two wheels 
			d = ( d_left + d_right ) / 2
			# this approximation works (in radians) for small angles
			# calculate velocities
			delta_thta = math.radians(float( ( d_right - d_left ) /  base_width ) )
			
			# calculate distance traveled in x and y
			# calculate the final position of the robot
			x =  x +  d * cos( delta_thta ) 
			y =  y +  d * sin( delta_thta ) 
			print "X: %s" %x
			print "Y: %s" %y
			
			print(c)

			th =  th + delta_thta
			print "th: %s" %th
			enc_left =  left
			enc_right =  right
			
			publish_Data(x , y, th)
			# print "left: %s" %left
			# print "enc_left: %s" %enc_right
			# print "right: %s" %right
			# print "enc_right: %s" %enc_right
			last_time = rospy.Time.now()
			c+=1
		left = c
		right = 3*c
	r.sleep()