#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import serial

class LidarNode(Node):
    def __init__(self):
        super().__init__("lidar_node")
        
        self.serial_port = serial.Serial(
            port='/dev/ttyS0',
            baudrate=230400,
            timeout=1
        )
        
        self.publisher = self.create_publisher(Int64, 'uart_rx', 10)
        self.get_logger().info("Lidar node initialized")
        self.create_timer(1/4500, self.read_uart)  
        
    def read_uart(self):
        try:
            if self.serial_port.in_waiting > 0:  # Checks if any bytes are in the buffer
                data = self.serial_port.read(self.serial_port.in_waiting)  # Reads this amount of bytes
                self.get_logger().info(f"Received: {data}") 
                
                msg_data = int.from_bytes(data, byteorder='big')
                
                msg = Int64()
                msg.data = msg_data
                self.publisher.publish(msg) 
        except Exception as e:
            self.get_logger().error(f"Error while reading UART: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = LidarNode()
    rclpy.spin(node) 
    rclpy.shutdown()

if __name__ == "__main__":
    main()
