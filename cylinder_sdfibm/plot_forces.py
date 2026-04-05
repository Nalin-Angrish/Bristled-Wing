import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

rho = 1.0 # fluid density (kg/m^3)
U_inf = 0.01 # free stream velocity (m/s)
D = 0.1 # characteristic length (m)
dz = 1 # grid spacing in z direction (m)

time = []
force_raw = []

with open("cloud.out", "r") as f:
    # Space separated values with no header
    # First column is time, sixth column is force

    for line in f:
        line = line.strip()
        parts = line.split()
        time.append(float(parts[0]))
        force_raw.append(float(parts[5]))

time = np.array(time)
force = np.array(force_raw)
total_duration = time[-1]

steady_state_force = np.mean(force[time > 0.9 * total_duration])

print(f"Steady State force = {steady_state_force:.6e}")
print(f"Coefficient of drag = {steady_state_force / (0.5 * rho * (U_inf**2) * D * dz):.6e}")

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

ax.plot(time, force, label="Force", color=plt.cm.tab10.colors[0], linewidth=1.4)
ax.plot(time, np.zeros(len(time)), color='#8b949e', linewidth=1.0, alpha=0.8)
ax.plot(time, np.ones(len(time)) * steady_state_force,
        label="Steady State Force", color=plt.cm.tab10.colors[1], linewidth=1.4)

ax.set_ylim(0, 5e-5)
ax.set_xlabel('Time [s]', color='#c9d1d9', fontsize=12)
ax.set_ylabel('Total Force (N)', color='#c9d1d9', fontsize=12)
ax.set_title('Total Force vs Time', color='#e6edf3', fontsize=13, pad=12)

ax.tick_params(colors='#8b949e')
for spine in ax.spines.values():
    spine.set_edgecolor('#30363d')

ax.grid(True, which='both', color='#21262d', linestyle='--', linewidth=0.6, alpha=0.8)
ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#c9d1d9', fontsize=10)

plt.tight_layout()
plt.savefig("force_v_time.png", dpi=150, bbox_inches='tight')
# plt.show()
