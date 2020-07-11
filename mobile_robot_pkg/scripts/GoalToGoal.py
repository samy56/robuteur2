#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from nav_msgs.msg import Odometry
import tf

class TurtleBot:
    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.velocity_publisher = rospy.Publisher('/cmd_vel',Twist , queue_size=10)
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(50)
    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscrib1er."""
        self.position = data.pose.pose.position
        self.orientation = data.pose.pose.orientation
        #self.pose = data
        self.robot_pose_x = round(self.position.x, 4)
        self.robot_pose_y = round(self.position.y, 4)
        self.roll, self.pitch, self.yaw = tf.transformations.euler_from_quaternion([self.orientation.x, self.orientation.y, self.orientation.z, self.orientation.w])
        

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.robot_pose_x), 2) + pow((goal_pose.y - self.robot_pose_y), 2))

    def linear_vel(self, goal_pose, constant=0.015):
        a = constant * self.euclidean_distance(goal_pose)
        if a>1:
            return 1
        else:
            return a

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.robot_pose_y, goal_pose.x - self.robot_pose_x)

    def angular_vel(self, goal_pose, constant=0.06):
        b = constant * (self.steering_angle(goal_pose) - self.pose.theta)
        if b>1:
            return 1
        else:
            return b

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
            #print "the value of x is %s" %self.robot_pose_x
            #print "the value of y is %s" %self.robot_pose_y
            #print "the value of theta is %s" %self.yaw
            print "the linear vel is %s" %vel_msg.linear.x
            print "the angular vel is %s" %vel_msg.angular.z
            print "the pos x is %s" %self.robot_pose_x
            print "the pos y %s" %self.robot_pose_y
            
           



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
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass