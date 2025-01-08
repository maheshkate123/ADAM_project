#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='image_obstacle_detection',
            executable='obstacle_detection.py',
            name='obstacle_detection_node',
            output='screen',
            parameters=[{
                'safe_distance': 0.5,
            }],
        ),
    ])
