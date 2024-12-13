from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='emage_motor_driver',
            executable='publisher_node',
            name='hello_world_publisher'
        ),
        Node(
            package='emage_motor_driver',
            executable='subscriber_node',
            name='hello_world_subscriber'
        )
    ])
