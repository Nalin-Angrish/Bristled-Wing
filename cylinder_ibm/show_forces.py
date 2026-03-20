import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def smooth_signal(data, window=101, poly=3):
    # window must be odd and <= len(data)
    if window >= len(data):
        window = len(data) - 1 if len(data) % 2 == 0 else len(data)
    if window % 2 == 0:
        window += 1

    return savgol_filter(data, window_length=window, polyorder=poly)

def ema_smooth(data, alpha=0.05):
    data = np.asarray(data)
    smoothed = np.zeros_like(data)

    smoothed[0] = data[0]

    for i in range(1, len(data)):
        smoothed[i] = alpha * data[i] + (1 - alpha) * smoothed[i-1]

    return smoothed

# choose direction index: 0 = x, 1 = y, 2 = z
direction = 0

time = []
force_raw = []

with open("forces/0/forces.dat", "r") as f:
    for line in f:
        line = line.strip()

        # skip comments
        if not line or line.startswith("#"):
            continue

        parts = line.replace("(", "").replace(")", "").split()

        # format: time | pressure(3) | viscous(3) | porous(3)
        t = float(parts[0])

        pressure = list(map(float, parts[1:4]))
        viscous = list(map(float, parts[4:7]))

        total_force = pressure[direction] + viscous[direction]

        time.append(t)
        force_raw.append(total_force)

time = np.array(time)
force_raw = np.array(force_raw)
force = smooth_signal(force_raw, window=1001, poly=1)
# force = ema_smooth(force_raw, 0.005)

total_duration = time[-1]

impulse_total = np.trapezoid(force_raw, time)
mean_force = impulse_total / total_duration

print(f"Mean force per cycle = {mean_force:.6e}")
print(f"Total impulse = {impulse_total:.6e}")


plt.figure()
plt.plot(time, force_raw, alpha=0.3, label="Raw Force")
plt.plot(time, force, label="Smoothed Force")
plt.plot(time, np.zeros(len(time)), 'k')
plt.plot(time, np.ones(len(time))*mean_force, label="Mean force per cycle")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Force (N)")
plt.title(f"Total Force vs Time")
plt.grid(True)
plt.ylim(-1, 0)
plt.show()
