import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS2!'
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: ' + msg.data)

def main():
    rclpy.init()
    node = Talker()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
