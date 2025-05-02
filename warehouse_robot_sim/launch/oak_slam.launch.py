# Requirements:
#   A Oak-D Pro Camera

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    start_localization = LaunchConfiguration('start_localization')
    parameters=[{
          'frame_id':'base_link',
          'subscribe_depth':True,
          'subscribe_odom_info':False,
          'approx_sync':True,
          'approx_sync_max_interval':0.02,
          'topic_queue_size':20,
          'sync_queue_size':10,
          'wait_imu_to_init':False,



          #Grid_mapping parameters
          'Grid/FromDepth':True,
          'Grid/EmptyRayTracing:':True ,
          'Grid/MaxObstacleHeight':'1.0',
          'Grid/MaxGroundHeight':'0.1',
          'Grid/3D':'false',
          'Reg/Force2D': 'true',
          'RGBD/OptimizeFrom3D': 'false',
          'Grid/RangeMax':'10.0',
          'Grid/RayTracing':'true',
          'Grid/Invert':'false',

          #RGBD-SLAM parameters 
          'RGBD/ProximityMaxGraphDepth': '0',
          'RGBD/ProximityPathMaxNeighbors': '1',
          'RGBD/ProximityBySpace': 'false',
          'RGBD/AngularUpdate': '0.05',
          'RGBD/LinearUpdate': '0.05',
          'RGBD/CreateOccupancyGrid':'true',
          'use_sim_time':True,
          'wait_for_transform':0.2,

          'database_path': '/home/emage/adam_ws/rtabmap.db',
        #   'localization': True,
          }]
        # If the localization parameter is true, RTAB-Map will attempt to localize the robot using the existing map (it will not create a new one).
    # Update the 'database_path' key
    localisation_parameters = parameters.copy()  # Make a copy if needed (optional)
    # localisation_parameters[0]['database_path'] = '/home/emage/adam_ws/src/rtabmap_emage.db'  # Update key

    remappings=[
        #   ('odom','/vodom'),
        #   ('imu', '/imu/data'),
          ('rgb/image', '/camera/color/image_raw'),
          ('rgb/camera_info', '/camera/color/camera_info'),
          ('depth/image', '/camera/depth/image_rect_raw')]

    return LaunchDescription([


  
        DeclareLaunchArgument(
            'start_localization', default_value='false',
            description='localization mode'),
        # Node(
        #     package='rtabmap_odom', executable='rgbd_odometry', output='screen',
        #     parameters=parameters,
        #     remappings=remappings),

        Node(
            condition=UnlessCondition(start_localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            name='rtabmap',
            parameters=parameters,
            remappings=remappings,
            arguments=['-d']),


        # Localization mode:
        Node(
            condition=IfCondition(start_localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            name='rtabmap',
            parameters=localisation_parameters,
            remappings=remappings,
            arguments = ['Mem/IncrementalMemory', 'False',
                         'Mem/InitWMWithAllNodes', 'True']),

        # Node(
        #     package='rtabmap_viz', executable='rtabmap_viz', output='screen',
        #     parameters=parameters,
        #     remappings=remappings),

        # Compute quaternion of the IMU
        # Node(
        #     package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
        #     parameters=[{'use_mag': False, 
        #                  'world_frame':'enu', 
        #                  'publish_tf':False}],
        #     remappings=[('imu/data_raw', '/oak/imu/data')]),
    ])
        