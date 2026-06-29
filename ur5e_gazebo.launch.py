from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import subprocess

def generate_launch_description():
    urdf = subprocess.check_output([
        'xacro',
        '/opt/ros/humble/share/ur_description/urdf/ur.urdf.xacro',
        'ur_type:=ur5e',
        'name:=ur',
        'prefix:='
    ]).decode('utf-8')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': urdf}]
        ),
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
    ])
