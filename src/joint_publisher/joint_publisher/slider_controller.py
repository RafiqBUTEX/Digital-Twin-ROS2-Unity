import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from rclpy.action import ActionClient
from builtin_interfaces.msg import Duration

class SliderController(Node):
    def __init__(self):
        super().__init__('slider_controller')
        self.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint',
            'elbow_joint', 'wrist_1_joint',
            'wrist_2_joint', 'wrist_3_joint'
        ]
        self.positions = [0.0] * 6
        self._action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory')

        # Subscribe to 6 topics
        for i, name in enumerate(self.joint_names):
            self.create_subscription(
                Float64,
                f'/unity_joint_command_{i}',
                lambda msg, idx=i: self.callback(msg, idx),
                10)
        self.get_logger().info('6-DOF Slider Controller ready!')

    def callback(self, msg, joint_idx):
        angle = (msg.data - 0.5) * 6.28
        self.positions[joint_idx] = angle
        self.get_logger().info(
            f'Joint {joint_idx} → {angle:.2f} rad')
        self.send_goal()

    def send_goal(self):
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = self.positions
        point.time_from_start = Duration(sec=1)
        goal.trajectory.points = [point]
        self._action_client.send_goal_async(goal)

def main():
    rclpy.init()
    node = SliderController()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
