from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
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
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    arguments=[
                        '-file', '/home/rafiq/ros2_ws/conveyor.urdf',
                        '-entity', 'conveyor',
                        '-x', '1.5', '-y', '0.0', '-z', '0.0'
                    ],
                    output='screen'
                )
            ]
        ),
    ])
