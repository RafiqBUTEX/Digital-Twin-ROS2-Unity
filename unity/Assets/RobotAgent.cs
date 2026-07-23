using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class RobotAgent : Agent
{
    public GameObject target;
    public GameObject robotEndEffector;
    private ArticulationBody[] joints;
    private float episodeReward = 0f;

    public override void Initialize()
    {
        joints = GetComponentsInChildren<ArticulationBody>();
    }

    public override void OnEpisodeBegin()
    {
        // Reset all joints to home position
        foreach (var joint in joints)
        {
            var drive = joint.xDrive;
            drive.target = 0f;
            joint.xDrive = drive;
        }

        // Randomize target position
        if (target != null)
        {
            target.transform.localPosition = new Vector3(
                Random.Range(-0.5f, 0.5f),
                Random.Range(0.3f, 0.8f),
                Random.Range(-0.5f, 0.5f)
            );
        }
        episodeReward = 0f;
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Target position
        if (target != null)
            sensor.AddObservation(target.transform.localPosition);
        else
            sensor.AddObservation(Vector3.zero);

        // Joint angles
        foreach (var joint in joints)
            sensor.AddObservation(joint.jointPosition[0]);

        // End effector position
        if (robotEndEffector != null)
            sensor.AddObservation(robotEndEffector.transform.localPosition);
        else
            sensor.AddObservation(Vector3.zero);
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        // Apply actions to joints
        for (int i = 0; i < Mathf.Min(actions.ContinuousActions.Length, joints.Length); i++)
        {
            var drive = joints[i].xDrive;
            drive.target += actions.ContinuousActions[i] * 10f;
            drive.target = Mathf.Clamp(drive.target, -180f, 180f);
            joints[i].xDrive = drive;
        }

        // Calculate reward
        if (target != null && robotEndEffector != null)
        {
            float distance = Vector3.Distance(
                robotEndEffector.transform.position,
                target.transform.position);

            // Reward for getting closer
            AddReward(-distance * 0.01f);

            // Big reward for reaching target
            if (distance < 0.1f)
            {
                AddReward(1f);
                EndEpisode();
            }
        }

        // Time penalty
        AddReward(-0.001f);
        episodeReward += GetCumulativeReward();
    }

    public override void Heuristic(in ActionBuffers actionsOut)
    {
        // Manual control for testing
        var actions = actionsOut.ContinuousActions;
        actions[0] = Input.GetAxis("Horizontal");
        actions[1] = Input.GetAxis("Vertical");
    }
}
