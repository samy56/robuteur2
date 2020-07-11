#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
from math import pow, atan2, sqrt


class Robuteur:
	def __init__(self):
		rospy.init_node('Robuteur_controller', anonymous=True)
		# Publisher which will publish to the topic '/turtle1/cmd_vel'.
		self.velocity_publisher = rospy.Publisher('/cmd_vel',Twist , queue_size=10)
		self.pose_subscriber = rospy.Subscriber('/pos',Pose2D, self.update_pose)
		self.pose = Pose()
		self.rate = rospy.Rate(2)

	def update_pose_angle(self, data):
		self.pose = data
		self.pose.x = round(self.pose.x, 4)
		self.pose.y = round(self.pose.y, 4)
		self.pose.theta = round(self.pose.theta, 4)

	def euclidean_distance(self, goal_pose):
		return sqrt(pow((goal_pose.x - self.pose.x), 2) +
					pow((goal_pose.y - self.pose.y), 2))

	def linear_vel(self, goal_pose, constant=1.5):
		#or try to make Linear vel constant but small
		return constant * self.euclidean_distance(goal_pose)

	def steering_angle(self, goal_pose):
		return math.atan( (goal_pose.y - self.pose.y / goal_pose.x - self.pose.x)  ) 

	def angular_vel(self, goal_pose, constant=6):
		return constant * math.atan2(self.steering_angle(goal_pose) - self.pose.theta)

	def move2goal(self):
		"""Moves the turtle to the goal."""
		goal_pose = Pose()
		# Get the input from the user.
		goal_pose.x = input("Set your x goal: ")
		goal_pose.y = input("Set your y goal: ")
		# Please, insert a number slightly greater than 0 (e.g. 0.01).
		distance_tolerance = input("Set your tolerance: ")
		vel_msg = Twist()

		while self.euclidean_distance(goal_pose) >= distance_tolerance:

			# Porportional controller.
			# Linear velocity in the x-axis.
			vel_msg.linear.x = self.linear_vel(goal_pose)
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0

			# Angular velocity in the z-axis.
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = self.angular_vel(goal_pose)

			# Publishing our vel_msg
			self.velocity_publisher.publish(vel_msg)

			# Publish at the desired rate.
			self.rate.sleep()

		# Stopping our robot after the movement is over.
		vel_msg.linear.x = 0
		vel_msg.angular.z = 0
		self.velocity_publisher.publish(vel_msg)

		# If we press control + C, the node will stop.
		rospy.spin()

if __name__ == '__main__':
	try:
		x = Robuteur()
		x.move2goal()
	except rospy.ROSInterruptException:
		pass