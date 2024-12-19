from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	ld = LaunchDescription()
	
	lidar_node = Node(
		package = "py_pkg",
		executable = "lidar_node"
	)
	
	imu_node = Node(
		package = "py_pkg",
		executable = "imu_node"
	)

	"""
	motor_node = Node(
		package = "cpp_pkg",
		executable = "motor_node"
	)
	"""
	
	ld.add_action(lidar_node)
	ld.add_action(imu_node)
	#ld.add_action(motor_node)
	
	return ld
