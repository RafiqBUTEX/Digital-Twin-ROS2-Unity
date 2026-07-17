import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

# Title
ax.text(7, 7.5, 'Digital Twin System Architecture — Bidirectional Control',
        ha='center', va='center', fontsize=14, fontweight='bold')

# Boxes
boxes = [
    (1.2, 4, 2, 1.2, '#2196F3', 'white', 'ROS2\nJoint Publisher\n(Python)'),
    (4.2, 4, 2, 1.2, '#FF9800', 'white', 'Gazebo\nSimulation\n(UR5e)'),
    (7.2, 4, 2, 1.2, '#9C27B0', 'white', 'ROS-TCP\nBridge\n(Endpoint)'),
    (10.2, 4, 2, 1.2, '#4CAF50', 'white', 'Unity 3D\nDigital Twin\n(C#)'),
    (4.2, 1.5, 2, 1.2, '#F44336', 'white', 'ROS2\nSlider Controller\n(Python)'),
    (10.2, 1.5, 2, 1.2, '#4CAF50', 'white', 'Unity\nUI Slider\n(C#)'),
]

for x, y, w, h, color, tcolor, label in boxes:
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='white',
                                    linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            color=tcolor, fontsize=9, fontweight='bold')

# Forward path arrows (top)
arrows_top = [
    (3.2, 4.6, 4.2, 4.6),
    (6.2, 4.6, 7.2, 4.6),
    (9.2, 4.6, 10.2, 4.6),
]
for x1, y1, x2, y2 in arrows_top:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

# Labels for forward path
ax.text(3.7, 4.9, '/joint_states', ha='center', fontsize=8, color='#333')
ax.text(6.7, 4.9, 'TCP', ha='center', fontsize=8, color='#333')
ax.text(9.7, 4.9, '/joint_states', ha='center', fontsize=8, color='#333')

# Bidirectional path arrows (bottom)
ax.annotate('', xy=(10.2, 2.1), xytext=(9.2, 2.1),
            arrowprops=dict(arrowstyle='<-', color='#F44336', lw=2))
ax.annotate('', xy=(6.2, 2.1), xytext=(7.2, 2.1),
            arrowprops=dict(arrowstyle='<-', color='#F44336', lw=2))
ax.annotate('', xy=(4.2, 2.1), xytext=(5.8, 2.1),
            arrowprops=dict(arrowstyle='<-', color='#F44336', lw=2))

# Labels for return path
ax.text(9.7, 2.4, '/unity_joint\n_command', ha='center', fontsize=8, color='#F44336')
ax.text(6.7, 2.4, 'TCP', ha='center', fontsize=8, color='#F44336')
ax.text(5.0, 2.4, 'action\nclient', ha='center', fontsize=8, color='#F44336')

# Legend
ax.text(1, 0.8, '→ Forward path (ROS2 → Unity)',
        fontsize=9, color='#333')
ax.text(1, 0.4, '→ Return path (Unity → Gazebo)',
        fontsize=9, color='#F44336')

plt.tight_layout()
plt.savefig('/home/rafiq/Desktop/architecture_diagram.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("Architecture diagram saved to Desktop!")
