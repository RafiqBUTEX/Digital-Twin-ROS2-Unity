# Unity-Based Digital Twin for UR5e 6-Axis Robotic Arm

**Author:** Md. Rafiqul Islam | BUTEX

## Overview
A real-time digital twin framework integrating ROS2 Humble with Unity 3D, enabling live synchronization of a UR5e 6-axis robotic arm between Gazebo simulation and Unity virtual environment.

## Objectives
- Build a real-time digital twin of a 6-axis industrial robotic arm
- Establish ROS2–Unity communication via TCP bridge
- Synchronize joint states between Gazebo and Unity at 10Hz
- Visualize live joint angles in Unity UI overlay

## Results
- ✅ UR5e arm fully simulated in Gazebo with joint trajectory controller
- ✅ Custom ROS2 joint state publisher (6 DOF, 10Hz)
- ✅ ROS2–Unity TCP bridge established via ROS-TCP-Connector
- ✅ Unity scene mirrors Gazebo in real time
- ✅ Live joint angle UI overlay in Unity Game view

## Tech Stack
ROS2 Humble · Ubuntu 22.04 · Unity 2022 LTS · Python · C# · URDF · Gazebo · ROS-TCP-Connector

## Demo
🎬 Video: https://youtu.be/644J21nwa-k
🌐 Portfolio: https://sites.google.com/view/md-rafiqul-islam-butex/featured-project

## Repository Structure
- `src/joint_publisher` — Custom 6-axis joint state publisher
- `src/talker_listener` — ROS2 pub/sub demo
- `src/ROS-TCP-Endpoint` — ROS2–Unity bridge
- `ur5e_gazebo.launch.py` — Gazebo launch file
