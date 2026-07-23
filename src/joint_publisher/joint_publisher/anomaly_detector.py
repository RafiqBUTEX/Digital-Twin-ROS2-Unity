import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import numpy as np

class AnomalyDetector(Node):
    def __init__(self):
        super().__init__('anomaly_detector')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.callback, 10)
        self.publisher = self.create_publisher(
            String, '/anomaly_alert', 10)
        
        # Normal range thresholds
        self.thresholds = {
            'shoulder_pan_joint': (-2.0, 2.0),
            'shoulder_lift_joint': (-2.0, 2.0),
            'elbow_joint': (-2.0, 2.0),
            'wrist_1_joint': (-2.0, 2.0),
            'wrist_2_joint': (-2.0, 2.0),
            'wrist_3_joint': (-2.0, 2.0)
        }
        self.get_logger().info('Anomaly Detector ready!')

    def callback(self, msg):
        anomalies = []
        for i, name in enumerate(msg.name):
            if name in self.thresholds:
                low, high = self.thresholds[name]
                if not (low <= msg.position[i] <= high):
                    anomalies.append(
                        f'{name}: {msg.position[i]:.2f}')

        alert = String()
        if anomalies:
            alert.data = 'ANOMALY: ' + ', '.join(anomalies)
            self.get_logger().warn(alert.data)
        else:
            alert.data = 'NORMAL'
        self.publisher.publish(alert)

def main():
    rclpy.init()
    node = AnomalyDetector()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
