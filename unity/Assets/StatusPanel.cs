using UnityEngine;
using TMPro;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using RosMessageTypes.Sensor;

public class StatusPanel : MonoBehaviour
{
    public TextMeshProUGUI robotStatus;
    public TextMeshProUGUI conveyorStatus;
    public TextMeshProUGUI anomalyAlert;
    private float lastJointUpdate = 0f;

    void Start()
    {
        ROSConnection.GetOrCreateInstance()
            .Subscribe<JointStateMsg>("/joint_states", UpdateRobotStatus);
        ROSConnection.GetOrCreateInstance()
            .Subscribe<StringMsg>("/conveyor/status", UpdateConveyorStatus);
        ROSConnection.GetOrCreateInstance()
            .Subscribe<StringMsg>("/anomaly_alert", UpdateAnomalyAlert);
    }

    void UpdateRobotStatus(JointStateMsg msg)
    {
        lastJointUpdate = Time.time;
        if (robotStatus != null)
            robotStatus.text = "Robot: ACTIVE ✓";
    }

    void UpdateConveyorStatus(StringMsg msg)
    {
        if (conveyorStatus != null)
            conveyorStatus.text = "Conveyor: " + msg.data;
    }

    void UpdateAnomalyAlert(StringMsg msg)
    {
        if (anomalyAlert != null)
        {
            anomalyAlert.text = msg.data;
            if (msg.data.Contains("ANOMALY"))
                anomalyAlert.color = Color.red;
            else
                anomalyAlert.color = Color.green;
        }
    }

    void Update()
    {
        if (Time.time - lastJointUpdate > 1f && robotStatus != null)
            robotStatus.text = "Robot: IDLE";
    }
}
