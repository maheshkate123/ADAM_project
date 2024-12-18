# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution

import xacro


def generate_launch_description():

       #aws_small_warehouse
    world = os.path.join(get_package_share_directory(
        'warehouse_robot_sim'), 'worlds', 'warehouse.world')
    
 
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'
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

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params,{'publish_frequency': 50.0}]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'TriOrb300P100',
                                    '-x', spawn_x_val,
                                    '-y', spawn_y_val,
                                    '-z', spawn_z_val,
                                    '-Y', spawn_yaw_val],
                        output='screen')

  




   


    rviz2= ExecuteProcess(cmd=['rviz2'],
            output="screen")

    return LaunchDescription([
        gazebo,
        spawn_entity,
        node_robot_state_publisher,
        # rviz2
         ])
