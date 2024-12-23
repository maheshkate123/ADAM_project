from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from launch.actions import AppendEnvironmentVariable
import os

def generate_launch_description():
    package_name = 'warehouse_robot_sim'
    urdf_file_name = 'TriOrb300P100.urdf'
    triorb_pkg_path = get_package_share_directory('warehouse_robot_sim')
    

    urdf = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        urdf_file_name)

    # Ensure the URDF file exists
    if not os.path.exists(urdf):
        raise FileNotFoundError(f'URDF file "{urdf}" does not exist!')

    return LaunchDescription([
        AppendEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=os.join(triorb_pkg_path, "models")),

        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'robot', '-file', urdf],
            output='screen'
        )
    ])

