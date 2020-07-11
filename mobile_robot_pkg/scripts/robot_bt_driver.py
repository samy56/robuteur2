#!/usr/bin/env python

'''
#File name:robot_bt_driver.py

#This is ROS driver node for mobile robot using bluetooth, it is using python bluetooth module for sending and receiving data.

#This will publish robot IMU, speed and encoder data, also send speed and reset command to robot

#Author: Lentin Joseph
'''
#ROS Modules
import rospy
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32 
from std_msgs.msg import Int32, Int64
from std_msgs.msg import Int32MultiArray
import threading  
import serial
import string
import time

import signal
import sys

##########################################################################################
global comPort
comPort = serial.Serial( port='/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
#comPort = serial.Serial( port='/dev/ttyACM1', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )	

##########################################################################################
rospy.init_node('ros_bluetooth_driver',anonymous=True)
orient = Vector3()

rospy.loginfo("Staring ROS-Bluetooth Driver node")

##########################################################################################
#Speed handler, this will send speed to BL
send_data = ''
def speed_send(data):
	global send_data
	#Note, here we may need change in one motor speed, now taking both speed as data
	try:
		#rospy.loginfo("I heard %s",data.data)
		left_speed = data.data[0]
		right_speed = data.data[1]

	except:
		rospy.logwarn("Found exception in BT driver node")
		print 'error in send data '
		left_speed = 0
		right_speed = 0	
		#print data.data[0]
		#rospy.loginfo( data.data[1]
		#print 'Setting left speed = %d : right speed=%d' %(left_speed,right_speed)
	send_data = 's %d %d\r' %(int(left_speed),int(right_speed))
	
	'''
	try:
		if comPort:
			comPort.write(send_data.encode())
			time.sleep(0.1)		
	except:
		rospy.logwarn("Unable to send Serial data")
		pass
		
		#Command to give as command line 
		
		rostopic pub /set_speed std_msgs/Int32MultiArray "layout:
		dim:
		- label: ''
			size: 0
			stride: 0
		data_offset: 0
		data: [50,50]"
		
##########################################################################################
'''
def reset_robot(data):	
	send_data = 'r\r'
	rospy.loginfo("Restting robot")
	try:
		if comPort:
			comPort.write(send_data.encode())
			rospy.sleep(0.01)
	except:
		rospy.logwarn("Unable to send Serila reset data")
		pass


##########################################################################################

#Publisher and subscriber list

left_speed_handle = rospy.Publisher('left_speed', Int32, queue_size=1)
right_speed_handle = rospy.Publisher('right_speed', Int32, queue_size=1)

left_encoder_handle = rospy.Publisher('left_ticks', Int32, queue_size=1)
right_encoder_handle = rospy.Publisher('right_ticks', Int32, queue_size=1)

imu_yaw_handle = rospy.Publisher('yaw', Float32, queue_size=1)
imu_pitch_handle = rospy.Publisher('pitch', Float32, queue_size=1)
imu_roll_handle = rospy.Publisher('roll', Float32, queue_size=1)

imu_data_handle = rospy.Publisher('imu_data', Vector3, queue_size=1)

ultrasonic_handle = rospy.Publisher('obstacle_distance', Int64, queue_size=1)

#Subscribers

    	
rospy.Subscriber('/set_speed', Int32MultiArray, speed_send)
#rospy.Subscriber('/reset', Int32, reset_robot)


def TransmitThread():	
	if comPort:
			comPort.write(send_data.encode())
			time.sleep(0.1)

def ReceiveThread():
	global receive_data
	if comPort.inWaiting() > 0:
		receive_data = comPort.readline()
		#print receive_data
		list_rec = receive_data.split("\n")
		list_rec = list(receive_data)
		#Continously receiving data from robot and decode it
		decode_string(list_rec)
			
	else:
		time.sleep(0.1)
		return 0



##########################################################################################

#Key board handler

def quit_code(signum, frame):

	# To reset the robot
	reset_robot(0)

	rospy.loginfo("Quitting code")
	sys.exit(1)

signal.signal(signal.SIGINT, quit_code)

##########################################################################################




#Function to publish topics to ROS
def publish_topics(string_list):
	global orient
	global left_speed_handle
	global right_speed_handle
	global left_encoder_handle
	global right_encoder_handle
	global imu_yaw_handle
	global imu_pitch_handle
	global imu_roll_handle
	global imu_data_handle
	global ultrasonic_handle
	#Reading each line in list and spliting it
	for line in string_list:
		real_data = line.split(" ")
		#print real_data
		if(real_data[0] == 's'):
			left_speed_handle.publish(float(real_data[1]))
			right_speed_handle.publish(float(real_data[2]))
		if(real_data[0] == 'e'):
			left_encoder_handle.publish(float(real_data[1]))
			right_encoder_handle.publish(float(real_data[2]))
		if(real_data[0] == 'i'):
			imu_yaw_handle.publish(float(real_data[1]))
			imu_pitch_handle.publish(float(real_data[2]))
			imu_roll_handle.publish(float(real_data[3]))


			orient.x = float(real_data[1])
			orient.y = float(real_data[2])
			orient.z = float(real_data[3])

			imu_data_handle.publish(orient)

		if(real_data[0] == 'u'):
			try:
				ultrasonic_handle.publish(int(real_data[1]))
			except:
				pass
##########################################################################################
#Function to remove spaces from sentence 



def remove_space(sentence):
	org_sentence = []
	for char in sentence:
		if(char != ""):
			org_sentence.append(char)

	#print org_sentence
	publish_topics(org_sentence)
	
##########################################################################################

def decode_string(string):
	'''This function will decode the buffer data and
	convert into each string which contain ypr values
	param: string, string buffer
	'''

	start_flag = 0

	final_string = ""

	string_list = []

	decode_list = list(string)
	string_len = len(decode_list)

	#IMU value extract
        
	for i in range(0,string_len):
		#Start reading when y is found
		if(decode_list[i] == 'i' and (string_len - i) > 10):
			start_flag = 1

		#Read until a carriage return occurs
		if(start_flag == 1):
			if(decode_list[i] != '\n'):
				final_string = final_string + decode_list[i]
			else:
				start_flag = 0
		#If it is a new line, append to a list
		if(decode_list[i] == "\n"):
			string_list.append(final_string)

			final_string = ''

	final_string = remove_space(string_list)


	string_list = []
	final_string  = ""
        #Encoder value extract
	for i in range(0,string_len):
		if(decode_list[i] == 'e' and (string_len - i) > 6):
			start_flag = 1

		if(start_flag == 1):
			if(decode_list[i] != '\n'):
				final_string = final_string + decode_list[i]
			else:
				start_flag = 0
		#If it is a new line, append to a list
		if(decode_list[i] == "\n"):
			string_list.append(final_string)

			final_string = ''
	
	final_string = remove_space(string_list)



	string_list = []
	final_string  = ""

        #Motor speed value extract
	for i in range(0,string_len):
		#Start reading when y is found
		if(decode_list[i] == 's' and (string_len - i) > 8):
			start_flag = 1

		if(start_flag == 1):
			if(decode_list[i] != '\n'):
				final_string = final_string + decode_list[i]
			else:
				start_flag = 0
		#If it is a new line, append to a list
		if(decode_list[i] == "\n"):
			string_list.append(final_string)

			final_string = ''	





	string_list = []
	final_string  = ""

        #Motor speed value extract
	for i in range(0,string_len):
		#Start reading when y is found
		if(decode_list[i] == 'u' and (string_len - i) > 4):
			start_flag = 1

		if(start_flag == 1):
			if(decode_list[i] != '\n'):
				final_string = final_string + decode_list[i]
			else:
				start_flag = 0
		#If it is a new line, append to a list
		if(decode_list[i] == "\n"):
			string_list.append(final_string)

			final_string = ''	




	final_string = remove_space(string_list)

##########################################################################################
#Function to connect to BL robot
	
##########################################################################################

#Main code

if __name__ == '__main__':
	
	while True: 
		threading.Thread(target=TransmitThread).start()
		threading.Thread(target=ReceiveThread).start()
		