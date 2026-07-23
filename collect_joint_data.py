import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import csv
import time

class DataCollector(Node):
    def __init__(self):
        super().__init__('data_collector')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.callback, 10)
        self.data = []
        self.start_time = time.time()
        self.get_logger().info('Collecting joint data...')

    def callback(self, msg):
        row = [time.time() - self.start_time] + list(msg.position)
        self.data.append(row)
        
        # Save every 100 samples
        if len(self.data) % 100 == 0:
            self.get_logger().info(f'Collected {len(self.data)} samples')
        
        # Stop after 500 samples
        if len(self.data) >= 500:
            self.save_data()
            rclpy.shutdown()

    def save_data(self):
        with open('/home/rafiq/ros2_ws/joint_data_normal.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'j0', 'j1', 'j2', 'j3', 'j4', 'j5'])
            writer.writerows(self.data)
        self.get_logger().info('Data saved to joint_data_normal.csv!')

def main():
    rclpy.init()
    node = DataCollector()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
