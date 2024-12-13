from setuptools import find_packages, setup

package_name = 'emage_motor_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/hello_world_launch.py']), 
        ('share/' + package_name + '/launch', ['launch/triorb_robot_launch.py']), 
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='deepak',
    maintainer_email='deepak@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_world_node = emage_motor_driver.hello_world_node:main',
            'publisher_node = emage_motor_driver.publisher_node:main',
            'subscriber_node = emage_motor_driver.subscriber_node:main',
            'triorb_robot_node = emage_motor_driver.triorb_robot_node:main', 
        ],
    },
)
