using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using System;
using System.Collections.Generic;

public class JointStateSubscriber : MonoBehaviour
{
    public GameObject robot;
    private ArticulationBody[] joints;
    private List<float> latencies = new List<float>();
    private float logTimer = 0f;

    void Start()
    {
        joints = robot.GetComponentsInChildren<ArticulationBody>();
        ROSConnection.GetOrCreateInstance().Subscribe<JointStateMsg>
            ("/joint_states", ReceiveJointState);
    }

private float lastReceiveTime = 0f;
private float lastPublishTime = 0f;

void ReceiveJointState(JointStateMsg msg)
{
    // Measure time between received messages (interval latency)
    float now = Time.realtimeSinceStartup;
    if (lastReceiveTime > 0f)
    {
        float intervalMs = (now - lastReceiveTime) * 1000f;
        latencies.Add(intervalMs);
    }
    lastReceiveTime = now;

    // Move joints
    for (int i = 0; i < msg.name.Length && i < joints.Length; i++)
    {
        var drive = joints[i].xDrive;
        drive.target = (float)(msg.position[i] * Mathf.Rad2Deg);
        joints[i].xDrive = drive;
    }
}

    void Update()
    {
        logTimer += Time.deltaTime;
        if (logTimer >= 5f && latencies.Count > 0)
        {
            float sum = 0;
            float min = float.MaxValue;
            float max = float.MinValue;
            foreach (float l in latencies)
            {
                sum += l;
                if (l < min) min = l;
                if (l > max) max = l;
            }
            float avg = sum / latencies.Count;
            Debug.Log($"Latency — Avg: {avg:F1}ms | Min: {min:F1}ms | " +
                     $"Max: {max:F1}ms | Samples: {latencies.Count}");
            latencies.Clear();
            logTimer = 0f;
        }
    }
}