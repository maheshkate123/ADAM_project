# ADAM Project : Emage TriOrb Robot
### Date - 11 Dec 2024
This repository contains development work for TriOrb robot Vison based navigation.

## Note - This repo should be cloned as src of the workspace and then name should be replaced from ADAM-TriOrb-Project to src in the ROS2 workspace 

Auto Build (useful in package testing)-
colcon build --symlink-install

### Running the robot in gazebo environment:
cd <your_ws>

source install/setup.bash

ros2 launch warehouse_robot_sim sim_launch.launch.py

### Utilities - 
Install - sudo apt install ros-humble-teleop-twist-keyboard
Run - ros2 run teleop_twist_keyboard teleop_twist_keyboard
