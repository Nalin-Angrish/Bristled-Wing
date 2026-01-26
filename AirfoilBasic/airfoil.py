import numpy as np
import matplotlib.pyplot as plt

# Configuration
typeNACA = input("Enter NACA 4-digit airfoil: ").strip()
grid_pts = 100

# Parse NACA digits
m = int(typeNACA[0]) / 100.0   # Max camber
p = int(typeNACA[1]) / 10.0    # Position of max camber
t = int(typeNACA[2:4]) / 100.0 # Max thickness

# Constants for thickness distribution
a0, a1, a2, a3, a4 = 0.2969, -0.1260, -0.3516, 0.2843, -0.1015

# 1. Generate Chord coordinates
beta = np.linspace(0, np.pi, grid_pts)
x = 0.5 * (1 - np.cos(beta))

# 2. Calculate Camber Line (yc) and Gradient (dyc/dx)
yc = np.zeros_like(x)
dyc_dx = np.zeros_like(x)

# Masking for vectorized conditional logic
front = x < p
back = x >= p

# Front of the airfoil
yc[front] = (m / p**2) * (2 * p * x[front] - x[front]**2)
dyc_dx[front] = (2 * m / p**2) * (p - x[front])

# Back of the airfoil
yc[back] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * x[back] - x[back]**2)
dyc_dx[back] = (2 * m / (1 - p)**2) * (p - x[back])

theta = np.arctan(dyc_dx)

# 3. Calculate Thickness Distribution (yt)
yt = 5 * t * (a0*np.sqrt(x) + a1*x + a2*x**2 + a3*x**3 + a4*x**4)

# 4. Calculate Surface Coordinates
xu = x - yt * np.sin(theta)
yu = yc + yt * np.cos(theta)
xl = x + yt * np.sin(theta)
yl = yc - yt * np.cos(theta)
x_coords = np.concatenate([xu[::-1], xl[1:]])
y_coords = np.concatenate([yu[::-1], yl[1:]])

# 5. Plotting
plt.figure(figsize=(10, 4))
plt.plot(x_coords, y_coords, 'bo', markersize=1, label='Upper Surface')
plt.plot(x, yc, 'g--', alpha=0.5, label='Mean Camber Line')
plt.axis('equal')
plt.grid(True)
plt.title(f'NACA {typeNACA} Profile')
plt.legend()
plt.show()

# 6. Save as GMSH format
with open("airfoil.geo", "w") as f:
    # Define points
    for i, (xi, yi) in enumerate(zip(x_coords, y_coords)):
        f.write(f"Point({i+1}) = {{{xi}, {yi}, 0}};\n")
    
    # Connect with a B-Spline for smoothness
    point_list = ", ".join([str(i+1) for i in range(len(x_coords))]) + ", 1"
    f.write(f"Line(1) = {{{point_list}}};\n")