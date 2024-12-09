#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from mpu6050 import mpu6050

class ImuNode(Node):
	def __init__(self):
		super().__init__("imu_node")
		self.get_logger().info("IMU node initialized")
		
		
def main(args=None):
	rclpy.init(args=args)
	node = ImuNode()
	rclpy.spin(node)	
	rclpy.shutdown()

if __name__ == "__main__":
	main()
