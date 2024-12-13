#!/usr/bin/env python3

import rclpy  # ROS 2 Python client library
from rclpy.node import Node  # Base class for creating nodes

# Define a class for the node
class HelloWorldNode(Node):
    def __init__(self):
        # Initialize the node with a name
        super().__init__('hello_world_node')  # Node name: 'hello_world_node'
        self.get_logger().info('Hello, World!')  # Log a "Hello, World!" message

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS 2 Python client library
    node = HelloWorldNode()  # Create an instance of the HelloWorldNode
    rclpy.spin(node)  # Keep the node alive until it is stopped
    node.destroy_node()  # Destroy the node when done
    rclpy.shutdown()  # Shutdown the ROS 2 system

if __name__ == '__main__':
    main()
