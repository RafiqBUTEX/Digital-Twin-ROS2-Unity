import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class JointPublisher(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        t = time.time() - self.start_time
        msg.name = ['shoulder_pan_joint', 'shoulder_lift_joint',
                    'elbow_joint', 'wrist_1_joint',
                    'wrist_2_joint', 'wrist_3_joint']
        msg.position = [
            math.sin(t * 0.5),
            math.sin(t * 0.4),
            math.sin(t * 0.3),
            math.sin(t * 0.2),
            math.sin(t * 0.1),
            math.sin(t * 0.6)
        ]
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = JointPublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
