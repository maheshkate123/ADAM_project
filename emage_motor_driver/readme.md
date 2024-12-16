## Emage Motor Driver Package 

This package contains - 
1. Robot hardware wrapper
2. ROS interface with hardware
3. Velocity and Odometry interface

Note - It Uses TriOrb / ROS2-msg-Types package to use structured msg and service types

### Build Package Dependencies 
#### Motor Lib
sudo python3 -m pip install git+https://github.com/TriOrb-Inc/triorb-core.git
#### Package deps
sudo apt-get install ros-humble-tf-transformations
rosdep install --from-paths src --ignore-src -r -y

### Make execuatable
chmod +x emage_motor_driver/emage_motor_driver/*

### Launch command 

#### Hello WOrld
ros2 launch emage_motor_driver hello_world_launch.py

#### Motor Driver Launch
ros2 launch emage_motor_driver triorb_robot_launch.py 

### Teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard
