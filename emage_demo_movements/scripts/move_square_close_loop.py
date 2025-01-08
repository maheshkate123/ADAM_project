#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from tf_transformations import euler_from_quaternion
import time


class DrawSquare(Node):
    def __init__(self):
        super().__init__('draw_square')
        self.publisher_=self.create_publisher(Twist,'/cmd_vel',10)
        self.odom_subscriber=self.create_subscription(Odometry,'/odom',self.odom_callback,10)
        self.side_length=2.0  # Length of each side of the square in meters
        self.linear_speed=0.2  # Linear speed in m/s
        self.angular_speed=0.3  # Angular speed in rad/s
        self.current_x=0.0
        self.current_y=0.0
        self.current_yaw=0.0
        self.initial_x=None
        self.initial_y=None
        self.initial_yaw=None

    def odom_callback(self, msg):
        # Extract position and orientation from odometry
        self.current_x=msg.pose.pose.position.x
        self.current_y=msg.pose.pose.position.y
        orientation_q=msg.pose.pose.orientation
        _,_,self.current_yaw=euler_from_quaternion([orientation_q.x,orientation_q.y,orientation_q.z,orientation_q.w])

    def move_straight(self, distance):
        # Save initial position
        self.initial_x=self.current_x
        self.initial_y=self.current_y
        msg=Twist()
        msg.linear.x=self.linear_speed
        while rclpy.ok():
            # Calculate distance traveled
            distance_traveled=math.sqrt((self.current_x-self.initial_x)**2+(self.current_y-self.initial_y)**2)
            if distance_traveled>=distance:
                break
            self.publisher_.publish(msg)
            rclpy.spin_once(self,timeout_sec=0.1)
        # Stop the robot
        msg.linear.x=0.0
        self.publisher_.publish(msg)

    def turn(self,angle):
        # Save initial yaw
        self.initial_yaw = self.current_yaw
        # Calculate target yaw
        target_yaw=(self.initial_yaw+angle)%(2*math.pi)
        if target_yaw>math.pi:
            target_yaw-=2*math.pi

        msg=Twist()
        msg.angular.z=self.angular_speed if angle > 0 else -self.angular_speed

        while rclpy.ok():
            # Check if the robot has turned enough
            yaw_error=abs(self.current_yaw-target_yaw)
            if yaw_error<0.05:  # Allowable error in radians
                break
            self.publisher_.publish(msg)
            rclpy.spin_once(self,timeout_sec=0.1)

        # Stop the robot
        msg.angular.z=0.0
        self.publisher_.publish(msg)

    def draw_square(self):
        for _ in range(4):
            # Move straight for the length of the square side
            self.move_straight(self.side_length)
            # Turn 90 degrees (pi/2 radians)
            self.turn(math.pi/2)
        self.get_logger().info("Finished drawing a square!")


def main(args=None):
    rclpy.init(args=args)
    node=DrawSquare()
    try:
        node.draw_square()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__=='__main__':
    main()
