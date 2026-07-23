import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Load normal data
print("Loading normal joint data...")
df = pd.read_csv('/home/rafiq/ros2_ws/joint_data_normal.csv')
print(f"Loaded {len(df)} samples")

# Features — all 6 joint angles
X = df[['j0', 'j1', 'j2', 'j3', 'j4', 'j5']].values

# Train Isolation Forest
print("Training anomaly detection model...")
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)
print("Model trained!")

# Test with normal data
normal_scores = model.decision_function(X)
normal_predictions = model.predict(X)
normal_anomalies = np.sum(normal_predictions == -1)
print(f"Normal data — Anomalies detected: {normal_anomalies}/{len(X)}")

# Simulate abnormal data
print("\nSimulating abnormal joint motion...")
X_abnormal = X.copy()
X_abnormal[:, 0] += 2.5  # Shift joint 0 significantly
X_abnormal[:, 2] += 3.0  # Shift joint 2 significantly

abnormal_predictions = model.predict(X_abnormal)
abnormal_anomalies = np.sum(abnormal_predictions == -1)
print(f"Abnormal data — Anomalies detected: {abnormal_anomalies}/{len(X_abnormal)}")

# Plot results
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Normal data
time = df['time'].values
axes[0].plot(time, X[:, 0], label='Joint 0', color='blue')
axes[0].plot(time, X[:, 2], label='Joint 2', color='green')
axes[0].set_title('Normal Joint Motion')
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Joint Angle (rad)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Anomaly scores
scores = model.decision_function(X_abnormal)
axes[1].plot(time, scores, color='red', label='Anomaly Score')
axes[1].axhline(y=0, color='black', linestyle='--', label='Threshold')
axes[1].fill_between(time, scores, 0,
                      where=(scores < 0),
                      color='red', alpha=0.3,
                      label='Anomaly Detected')
axes[1].set_title('Anomaly Detection on Abnormal Joint Motion')
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Anomaly Score')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/rafiq/Desktop/anomaly_detection.png', dpi=150)
plt.show()
print("\nAnomaly detection plot saved to Desktop!")
