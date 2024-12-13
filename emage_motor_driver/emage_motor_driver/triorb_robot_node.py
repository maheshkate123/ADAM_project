import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf_transformations import quaternion_from_euler
import logging
from triorb_core import robot as TriOrbRobot
from triorb_core import TriOrbDrive3Pose
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")

class TriOrbRobotNode(Node):
    def __init__(self):
        super().__init__('triorb_robot_node')

        self.declare_parameter('robot_port', '/dev/ttyUSB0') 
        # Get the robot port from the parameters
        robot_port = self.get_parameter('robot_port').get_parameter_value().string_value
        self.get_logger().info(f"Initializing the TriOrb Robot on port: {robot_port}")

        if not os.path.exists(robot_port):
            self.get_logger().error(f"Port {robot_port} not found.")
            self.shutdown_node("Shutting down Robot Node, since port is not available.")  # Shutdown node gracefully
            return

        # Initialize the robot
        try:
            self.robot = TriOrbRobot(robot_port)
            self.get_logger().info("Robot initialized successfully!")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize the robot: {e}")
            self.shutdown_node("Robot initialization failed.")  # Shutdown node gracefully
            return

        # ROS publishers and subscribers
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # TF broadcaster
        self.odom_broadcaster = TransformBroadcaster(self)

        # Parameters for robot state
        self.last_time = self.get_clock().now()
        self.x, self.y, self.theta = 0.0, 0.0, 0.0
        self.vel_x, self.vel_y, self.omega = 0.0, 0.0, 0.0

        # Timer to publish odometry at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_odometry) 

    def cmd_vel_callback(self, msg):
        """Callback for /cmd_vel to set robot velocity."""
        # Convert ROS frame velocities to robot frame velocities
        self.vel_x = msg.linear.y
        self.vel_y = msg.linear.x
        self.omega = msg.angular.z

        self.get_logger().info(f"Publishing cmd_vel to robot: x:{self.vel_x}, y:{self.vel_y}, w:{self.omega}")
        try:
            self.robot.set_vel_absolute(self.vel_x, self.vel_y, self.omega, acc=500, dec=500)
        except Exception as e:
            self.get_logger().error(f"Error setting velocity: {e}")

    def publish_odometry(self):
        """Publishes odometry information."""

        current_time = self.get_clock().now()
        self.get_logger().info(f"Publishing odom at time : {current_time}")

        # Get robot pose in its local frame
        robot_pose: TriOrbDrive3Pose = self.robot.get_pos()[0]

        # Convert robot frame coordinates to ROS frame
        ros_x = robot_pose.y  # Robot's +y becomes ROS's +x
        ros_y = robot_pose.x  # Robot's +x becomes ROS's +y
        ros_theta = robot_pose.w

        # Create odometry message
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = "odom"

        # Pose
        odom.pose.pose.position.x = ros_x
        odom.pose.pose.position.y = ros_y
        odom.pose.pose.position.z = 0.0
        quaternion = quaternion_from_euler(0, 0, ros_theta)
        odom.pose.pose.orientation.x = quaternion[0]
        odom.pose.pose.orientation.y = quaternion[1]
        odom.pose.pose.orientation.z = quaternion[2]
        odom.pose.pose.orientation.w = quaternion[3]

        # Velocity
        odom.child_frame_id = "base_link"
        odom.twist.twist.linear.x = self.vel_y  # Robot's +x velocity becomes ROS's +y
        odom.twist.twist.linear.y = self.vel_x  # Robot's +y velocity becomes ROS's +x
        odom.twist.twist.angular.z = self.omega

        # Publish odometry
        self.odom_pub.publish(odom)

        # Broadcast transform
        transform = TransformStamped()
        transform.header.stamp = current_time.to_msg()
        transform.header.frame_id = "odom"
        transform.child_frame_id = "base_link"
        transform.transform.translation.x = ros_x
        transform.transform.translation.y = ros_y
        transform.transform.translation.z = 0.0
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]

        # Send the transform
        self.odom_broadcaster.sendTransform(transform)

        self.last_time = current_time

    def shutdown_node(self, msg):
        """Shutdown the node gracefully with a custom message."""
        self.get_logger().error(msg)
        self.destroy_node()
        try:
            rclpy.shutdown()  # Safe shutdown attempt
        except RuntimeError:
            pass  # Ignore error if rclpy is not initialized
        exit(1)  # Optionally, exit with a non-zero status to indicate failure

def main(args=None):
    rclpy.init(args=args)
    try:
        robot_node = TriOrbRobotNode()
        rclpy.spin(robot_node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            rclpy.shutdown()  # Safe shutdown attempt
        except RuntimeError:
            pass  # Ignore error if rclpy is not initialized

if __name__ == "__main__":
    main()
