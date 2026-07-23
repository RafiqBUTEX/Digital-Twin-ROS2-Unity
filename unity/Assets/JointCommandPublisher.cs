using UnityEngine;
using UnityEngine.UI;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using System.Collections;

public class JointCommandPublisher : MonoBehaviour
{
    ROSConnection ros;
    public Slider[] jointSliders = new Slider[6];
    public Slider conveyorSlider;
    private float[] lastValues = new float[6];
    private float lastConveyorValue = 0f;

 IEnumerator Start()
{
    yield return new WaitForSeconds(3f);
    ros = ROSConnection.GetOrCreateInstance();
    for (int i = 0; i < 6; i++)
    {
        ros.RegisterPublisher<Float64Msg>($"/unity_joint_command_{i}");
        lastValues[i] = 0f;
    }
    ros.RegisterPublisher<Float64Msg>("/unity_conveyor_command");
}

    void Update()
    {
        // Joint sliders
        for (int i = 0; i < 6; i++)
        {
            if (jointSliders[i] != null &&
                Mathf.Abs(jointSliders[i].value - lastValues[i]) > 0.01f)
            {
                Float64Msg msg = new Float64Msg();
                msg.data = jointSliders[i].value;
                ros.Publish($"/unity_joint_command_{i}", msg);
                lastValues[i] = jointSliders[i].value;
            }
        }

        // Conveyor slider
        if (conveyorSlider != null &&
            Mathf.Abs(conveyorSlider.value - lastConveyorValue) > 0.01f)
        {
            Float64Msg msg = new Float64Msg();
            msg.data = (conveyorSlider.value - 0.5f) * 2f;
            ros.Publish("/unity_conveyor_command", msg);
            lastConveyorValue = conveyorSlider.value;
        }
    }
}