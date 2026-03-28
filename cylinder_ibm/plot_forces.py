import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

rho = 1.0 # fluid density (kg/m^3)
U_inf = 0.01 # free stream velocity (m/s)
D = 0.1 # characteristic length (m)
dz = 0.02 # grid spacing in z direction (m)

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

        total_force = pressure[0] + viscous[0]

        time.append(t)
        force_raw.append(total_force)

time = np.array(time)
force = np.array(force_raw)
total_duration = time[-1]

steady_state_force = np.mean(force[time > 0.9 * total_duration])

print(f"Steady State force = {steady_state_force:.6e}")
print(f"Coefficient of drag = {steady_state_force / (0.5 * rho * (U_inf**2) * D * dz):.6e}")

plt.figure()
plt.plot(time, force, label="Force")
plt.plot(time, np.zeros(len(time)), 'k')
plt.plot(time, np.ones(len(time))*steady_state_force, label="Steady State Force")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Force (N)")
plt.title(f"Total Force vs Time")
plt.grid(True)
plt.ylim(-1e-5, 1e-5)
plt.savefig("force_v_time.png", dpi=300)
