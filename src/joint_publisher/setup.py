from setuptools import find_packages, setup

package_name = 'joint_publisher'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rafiq',
    maintainer_email='rafiq@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'joint_publisher = joint_publisher.joint_publisher:main',
            'slider_controller = joint_publisher.slider_controller:main',
            'conveyor_controller = joint_publisher.conveyor_controller:main',
            'anomaly_detector = joint_publisher.anomaly_detector:main',
            'moveit_commander = joint_publisher.moveit_commander:main',
        ],
    },
)
