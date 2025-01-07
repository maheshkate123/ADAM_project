#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import numpy as np
from cv_bridge import CvBridge


class ObstacleDetectionNode(Node):
    def __init__(self):
        super().__init__('obstacle_detection_node')
        self.safe_distance = 0.5
        self.bridge = CvBridge()
        self.depth_sub = self.create_subscription(
            Image, '/camera/depth/image_rect_raw', self.depth_callback, 10
        )
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.object_detected = False
        self.in_cooldown = False

        # Timer to continuously send velocity commands
        self.timer = self.create_timer(0.1, self.move_forward)

        # Cooldown timer
        self.cooldown_timer = None

    def depth_callback(self, msg):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            depth_array = np.array(depth_image, dtype=np.float32)
            height, width = depth_array.shape

            # Define the region of interest (ROI) to cover a wider area
            top = height // 3
            bottom = 2 * height // 3
            left = width // 4  # Expanded left boundary
            right = 3 * width // 4  # Expanded right boundary

            # Extract the ROI from the depth array
            roi = depth_array[top:bottom, left:right]
            min_distance = np.nanmin(roi)

            # Check if an object is within the safe distance
            if min_distance < self.safe_distance:
                if not self.object_detected:
                    self.get_logger().info(f"Object detected at {min_distance:.2f}m. Stopping robot.")
                self.object_detected = True
                self.stop_robot()

                # Start cooldown timer if not already in cooldown
                if not self.in_cooldown:
                    self.start_cooldown()

            else:
                if self.object_detected and not self.in_cooldown:
                    self.get_logger().info("Path is clear. Resuming forward motion.")
                self.object_detected = False

        except Exception as e:
            self.get_logger().error(f"Error processing depth image: {e}")

    def move_forward(self):
        if not self.object_detected and not self.in_cooldown:
            forward_msg = Twist()
            forward_msg.linear.x = 1.0  
            self.cmd_vel_pub.publish(forward_msg)

    def stop_robot(self):
        """Stops the robot."""
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)

    def start_cooldown(self):
        """Starts a cooldown period to prevent immediate forward motion."""
        self.in_cooldown = True
        self.cooldown_timer = self.create_timer(2.0, self.end_cooldown)  # 2 seconds cooldown

    def end_cooldown(self):
        self.in_cooldown = False
        if self.cooldown_timer:
            self.cooldown_timer.cancel()  # Stop the cooldown timer
            self.cooldown_timer = None


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node.")
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        node.destroy_node()


if __name__ == '__main__':
    main()

