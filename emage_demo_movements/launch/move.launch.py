#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node(
        #     package='emage_demo_movements',
        #     executable='move_square.py',
        #     name='move_node',
        #     output='screen',
        #     parameters=[{
                
        #     }],
        # ),

        Node(
            package='emage_demo_movements',
            executable='move_square_close_loop.py',
            name='move_node_close_loop',
            output='screen',
            parameters=[{
                
            }],
        ),
    ])
