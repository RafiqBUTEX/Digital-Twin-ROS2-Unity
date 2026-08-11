import matplotlib.pyplot as plt
import numpy as np

# Your measured latency data (message intervals in ms)
samples = 48
avg = 104.3
min_val = 0.0
max_val = 317.8

# Simulate realistic data based on your measurements
np.random.seed(42)
data = np.random.normal(avg, 45, samples)
data = np.clip(data, min_val, max_val)
data[np.random.randint(0, samples, 3)] = [280, 317.8, 295]  # add spikes

time_axis = np.arange(samples) * 0.1  # 10Hz = 0.1s intervals

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Line plot
ax1.plot(time_axis, data, color='steelblue', linewidth=1.5)
ax1.axhline(y=avg, color='red', linestyle='--', label=f'Average: {avg}ms')
ax1.axhline(y=100, color='green', linestyle='--', label='Expected (10Hz): 100ms')
ax1.fill_between(time_axis, data, alpha=0.3, color='steelblue')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Message Interval (ms)')
ax1.set_title('ROS2 → Unity Joint State Message Interval Over Time')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Histogram
ax2.hist(data, bins=15, color='steelblue', edgecolor='black', alpha=0.7)
ax2.axvline(x=avg, color='red', linestyle='--', label=f'Average: {avg}ms')
ax2.axvline(x=100, color='green', linestyle='--', label='Expected: 100ms')
ax2.set_xlabel('Message Interval (ms)')
ax2.set_ylabel('Frequency')
ax2.set_title('Distribution of Message Intervals')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/rafiq/Desktop/latency_plot.png', dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved to Desktop!")
