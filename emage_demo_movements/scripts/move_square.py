#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math

class DrawSquare(Node):
    def __init__(self):
        super().__init__('draw_square')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.side_length = 2.0  # Length of each side of the square in meters
        self.linear_speed = 0.5  # Speed of the robot in m/s
        self.angular_speed = 1.0  # Speed of rotation in rad/s

    def move_straight(self, duration):
        msg = Twist()
        msg.linear.x = self.linear_speed
        self.publisher_.publish(msg)
        time.sleep(duration)
        msg.linear.x = 0.0
        self.publisher_.publish(msg)

    def turn_right(self):
        msg = Twist()
        msg.angular.z = -self.angular_speed  # Turning right (counter-clockwise in most cases)
        self.publisher_.publish(msg)
        # Turn for 90 degrees (1.5708 radians), now we double the time taken
        turn_duration = (math.pi / 2) / self.angular_speed * 2.5  # Double the time
        time.sleep(turn_duration)
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def draw_square(self):
        for _ in range(4):
            # Move straight for the length of the square side
            self.move_straight(self.side_length / self.linear_speed)
            # Turn right (90 degrees)
            self.turn_right()
        self.get_logger().info("Finished drawing a square!")

def main(args=None):
    rclpy.init(args=args)
    node = DrawSquare()
    node.draw_square()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

