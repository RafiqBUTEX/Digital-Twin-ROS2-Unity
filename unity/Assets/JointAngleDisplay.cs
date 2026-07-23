using UnityEngine;
using TMPro;
using Unity.Robotics.UrdfImporter;

public class JointAngleDisplay : MonoBehaviour
{
    public GameObject robot;          // drag your "ur" GameObject here
    public TextMeshProUGUI displayText; // drag JointAngleText here

    private ArticulationBody[] joints;
    private string[] jointNames = {
        "shoulder_pan_joint",
        "shoulder_lift_joint",
        "elbow_joint",
        "wrist_1_joint",
        "wrist_2_joint",
        "wrist_3_joint"
    };

    void Start()
    {
        joints = robot.GetComponentsInChildren<ArticulationBody>();
    }

    void Update()
    {
        string output = "Joint Angles (deg):\n";
        foreach (var body in joints)
        {
            if (body.jointType == ArticulationJointType.RevoluteJoint)
            {
                float angleRad = body.jointPosition.dofCount > 0 ? body.jointPosition[0] : 0f;
                float angleDeg = angleRad * Mathf.Rad2Deg;
                output += $"{body.name}: {angleDeg:F1}°\n";
            }
        }
        displayText.text = output;
    }
}
