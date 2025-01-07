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

        # Timer to continuously send velocity commands
        self.timer = self.create_timer(0.1, self.move_forward)

    def depth_callback(self, msg):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            depth_array = np.array(depth_image, dtype=np.float32)
            height, width = depth_array.shape

            # Extract the center region of the depth image
            center_region = depth_array[height // 3 : 2 * height // 3, width // 3 : 2 * width // 3]
            min_distance = np.nanmin(center_region)

            # Check if an object is within the safe distance
            if min_distance < self.safe_distance:
                if not self.object_detected:
                    self.get_logger().info(f"Object detected at {min_distance:.2f}m. Stopping robot.")
                self.object_detected = True
                self.stop_robot()
            else:
                if self.object_detected:
                    self.get_logger().info("Path is clear. Resuming forward motion.")
                self.object_detected = False

        except Exception as e:
            self.get_logger().error(f"Error processing depth image: {e}")

    def move_forward(self):
        if not self.object_detected:
            forward_msg = Twist()
            forward_msg.linear.x = 1.0  # Set a forward speed
            self.cmd_vel_pub.publish(forward_msg)

    def stop_robot(self):
        """Stops the robot."""
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)


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
