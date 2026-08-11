import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, BoundingVolume
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient

class MoveItCommander(Node):
    def __init__(self):
        super().__init__('moveit_commander')
        self.subscription = self.create_subscription(
            Float64MultiArray,
            '/unity_target_pose',
            self.callback,
            10)
        self._action_client = ActionClient(
            self, MoveGroup, '/move_action')
        self._send_goal_future = None
        self.get_logger().info('MoveIt Commander ready!')

    def callback(self, msg):
        self.get_logger().info(f'Received target: {msg.data}')
        ros_x = msg.data[2]
        ros_y = -msg.data[0]
        ros_z = msg.data[1]
        converted = list(msg.data)
        converted[0] = ros_x
        converted[1] = ros_y
        converted[2] = ros_z
        self.send_goal(converted)

    def send_goal(self, data):
        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = 'ur_manipulator'
        goal_msg.request.num_planning_attempts = 10
        goal_msg.request.allowed_planning_time = 10.0
        goal_msg.request.max_velocity_scaling_factor = 0.5
        goal_msg.request.max_acceleration_scaling_factor = 0.5

        pose = PoseStamped()
        pose.header.frame_id = 'world'
        pose.pose.position.x = data[0]
        pose.pose.position.y = data[1]
        pose.pose.position.z = data[2]
        pose.pose.orientation.x = data[3]
        pose.pose.orientation.y = data[4]
        pose.pose.orientation.z = data[5]
        pose.pose.orientation.w = data[6]

        pos_constraint = PositionConstraint()
        pos_constraint.header.frame_id = 'world'
        pos_constraint.link_name = 'tool0'
        pos_constraint.target_point_offset.x = 0.0
        pos_constraint.target_point_offset.y = 0.0
        pos_constraint.target_point_offset.z = 0.0

        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.SPHERE
        primitive.dimensions = [0.01]

        bv = BoundingVolume()
        bv.primitives.append(primitive)
        bv.primitive_poses.append(pose.pose)
        pos_constraint.constraint_region = bv
        pos_constraint.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints.append(pos_constraint)
        goal_msg.request.goal_constraints.append(constraints)

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info('Goal accepted!')
            self._get_result_future = goal_handle.get_result_async()
            self._get_result_future.add_done_callback(self.result_callback)
        else:
            self.get_logger().warn('Goal rejected!')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.error_code}')
        self.get_logger().info('Ready for next goal!')
        self._send_goal_future = None

def main():
    rclpy.init()
    node = MoveItCommander()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
