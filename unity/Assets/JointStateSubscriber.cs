using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using Unity.Robotics.UrdfImporter.Control;

public class JointStateSubscriber : MonoBehaviour
{
    public GameObject robot;
    private ArticulationBody[] joints;

    void Start()
    {
        joints = robot.GetComponentsInChildren<ArticulationBody>();
        ROSConnection.GetOrCreateInstance().Subscribe<JointStateMsg>("/joint_states", ReceiveJointState);
    }

    void ReceiveJointState(JointStateMsg msg)
    {
        for (int i = 0; i < msg.name.Length && i < joints.Length; i++)
        {
            var drive = joints[i].xDrive;
            drive.target = (float)(msg.position[i] * Mathf.Rad2Deg);
            joints[i].xDrive = drive;
        }
    }
}