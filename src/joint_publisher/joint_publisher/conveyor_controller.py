import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String
import math
import time

class ConveyorController(Node):
    def __init__(self):
        super().__init__('conveyor_controller')
        
        # Publisher for belt position
        self.belt_pub = self.create_publisher(
            Float64, '/conveyor/belt_position', 10)
        
        # Publisher for conveyor status
        self.status_pub = self.create_publisher(
            String, '/conveyor/status', 10)
        
        # Subscribe to Unity conveyor command
        self.create_subscription(
            Float64, '/unity_conveyor_command',
            self.command_callback, 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.speed = 0.0
        self.position = 0.0
        self.start_time = time.time()
        self.get_logger().info('Conveyor Controller ready!')

    def command_callback(self, msg):
        self.speed = msg.data
        self.get_logger().info(f'Conveyor speed: {self.speed:.2f}')

    def timer_callback(self):
        # Update belt position
        self.position += self.speed * 0.1
        self.position = max(-0.9, min(0.9, self.position))
        
        # Publish belt position
        pos_msg = Float64()
        pos_msg.data = self.position
        self.belt_pub.publish(pos_msg)
        
        # Publish status
        status_msg = String()
        if abs(self.speed) > 0.01:
            status_msg.data = f'RUNNING | Speed: {self.speed:.2f} | Position: {self.position:.2f}'
        else:
            status_msg.data = 'STOPPED'
        self.status_pub.publish(status_msg)

def main():
    rclpy.init()
    node = ConveyorController()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
