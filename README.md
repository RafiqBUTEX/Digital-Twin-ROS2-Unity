# Unity-Based Digital Twin for 6-Axis Robotic Arm with ROS2

**ASML Lab Collaboration | University of North Texas (Remote)**  
**Author:** Md. Rafiqul Islam | May 2026 – Present

## Project Overview
Real-time digital twin of a UR5e 6-axis robotic arm integrating 
ROS2 Humble with Unity 3D via ROS-TCP-Connector bridge.

## Tech Stack
- ROS2 Humble | Ubuntu 22.04
- Unity 2022 LTS | C#
- Python | URDF | Gazebo
- ROS-TCP-Connector

## Progress
- ✅ Week 1: ROS2 setup, turtlesim, talker/listener, 6-axis arm in RViz
- ✅ Week 2: Gazebo simulation, UR5e spawned, ROS2-Unity bridge
- 🔄 Week 3: Unity digital twin synchronization (in progress)

## Repository Structure
- `src/talker_listener` - ROS2 pub/sub demo
- `src/joint_publisher` - 6-axis joint state publisher
- `src/ROS-TCP-Endpoint` - ROS2-Unity bridge
