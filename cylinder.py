import numpy as np

r = 0.05  # radius
n = 100
z1, z2 = -0.01, 0.01
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
x = r * np.cos(theta)
y = r * np.sin(theta)

cases = ['cylinder_ibm']

for case in cases:
    with open(case + "/constant/triSurface/cylinder.stl", "w") as f:
        f.write("solid cylinder\n")
        for i in range(n):
            i2 = (i + 1) % n
            # front face
            f.write(f"  facet normal 0 0 -1\n    outer loop\n")
            f.write(f"      vertex 0 0 {z1}\n")
            f.write(f"      vertex {x[i]} {y[i]} {z1}\n")
            f.write(f"      vertex {x[i2]} {y[i2]} {z1}\n")
            f.write(f"    endloop\n  endfacet\n")
            # back face
            f.write(f"  facet normal 0 0 1\n    outer loop\n")
            f.write(f"      vertex 0 0 {z2}\n")
            f.write(f"      vertex {x[i2]} {y[i2]} {z2}\n")
            f.write(f"      vertex {x[i]} {y[i]} {z2}\n")
            f.write(f"    endloop\n  endfacet\n")
            # side faces
            f.write(f"  facet normal {np.cos((theta[i]+theta[i2])/2)} {np.sin((theta[i]+theta[i2])/2)} 0\n    outer loop\n")
            f.write(f"      vertex {x[i]} {y[i]} {z1}\n")
            f.write(f"      vertex {x[i2]} {y[i2]} {z1}\n")
            f.write(f"      vertex {x[i2]} {y[i2]} {z2}\n")
            f.write(f"    endloop\n  endfacet\n")
            f.write(f"  facet normal {np.cos((theta[i]+theta[i2])/2)} {np.sin((theta[i]+theta[i2])/2)} 0\n    outer loop\n")
            f.write(f"      vertex {x[i]} {y[i]} {z1}\n")
            f.write(f"      vertex {x[i2]} {y[i2]} {z2}\n")
            f.write(f"      vertex {x[i]} {y[i]} {z2}\n")
            f.write(f"    endloop\n  endfacet\n")
        f.write("endsolid cylinder\n")