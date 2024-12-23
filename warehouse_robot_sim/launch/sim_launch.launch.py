import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():

      
    world = os.path.join(get_package_share_directory(
        'warehouse_robot_sim'), 'worlds', 'warehouse.world')
    
 
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.025'
    spawn_yaw_val = '0.0'
    


    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),launch_arguments={'world':world}.items()
             )

    robot_path = os.path.join(
        get_package_share_directory('warehouse_robot_sim'))

    xacro_file = os.path.join(robot_path,
                              'urdf',
                              'TriBot_Oakd.urdf.xacro')

    # Parse the xacro file
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    # Define nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params, {'publish_frequency': 50.0}]
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'TriOrb300P100',
            '-x', spawn_x_val,
            '-y', spawn_y_val,
            '-z', spawn_z_val,
            '-Y', spawn_yaw_val
        ],
        output='screen'
    )

    rviz2 = ExecuteProcess(cmd=['rviz2'], output="screen")

    return LaunchDescription([
        # Set the GAZEBO_MODEL_PATH environment variable
        SetEnvironmentVariable(
            name='GAZEBO_MODEL_PATH',
            value=os.path.join(robot_path, "models")
        ),
        gazebo,
        spawn_entity,
        node_robot_state_publisher,
        # Uncomment RViz if needed
        # rviz2
    ])

