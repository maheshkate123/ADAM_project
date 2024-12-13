
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node 
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Declare the launch argument 'robot_port'
        DeclareLaunchArgument('robot_port', default_value='/dev/ttyACM0', description='The serial port for the robot'),

        # Log information about the launch
        LogInfo(
            condition=None,
            msg="Launching TriOrbRobotNode..."),

        # Node declaration with 'robot_port' parameter passed from the launch file
        Node(
            package='emage_motor_driver',
            executable='triorb_robot_node',  # This should be the executable for your node
            name='triorb_robot_node',
            output='screen',
            parameters=[{
                'robot_port': LaunchConfiguration('robot_port'),
            }],
            remappings=[('/cmd_vel', '/cmd_vel'),  # Add any topic remapping here if necessary
                        ('/odom', '/odom')],
        ),
    ])

