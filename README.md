# CFD-Based Modeling of Bristled Wings in Low Reynolds Number Regimes

This repository contains the code, simulation cases, and resources for a project studying the aerodynamic performance of bristled wings using the **Immersed Boundary Method (IBM)** implemented in OpenFOAM. The work targets the featherwing beetle *Paratuposa placentis*, one of the smallest known flying insects (Re ≈ 60), whose hindwings consist of a central rachis fringed with bristles rather than a continuous membrane.

## Overview

At the scales relevant to tiny insects, viscous forces dominate and the inter-bristle flow structure governs aerodynamic force production. Traditional body-fitted meshing approaches become prohibitively expensive for moving boundaries like flapping bristled wings. This project uses the **sdfibm** solver — a Signed Distance Field based discrete-forcing IBM — to avoid costly remeshing while accurately imposing no-slip conditions on moving surfaces.

No prior study has applied IBM within OpenFOAM to the bristled wing problem with species-specific kinematics of *P. placentis*. This project validates the IBM approach against canonical benchmarks as a precursor to simulating the full bristled wing geometry.

## Solver: sdfibm (not foam-extend)

We use a slightly modified version of [sdfibm](https://github.com/Nalin-Angrish/sdfibm) by Zhang et al. instead of foam-extend's built-in IBM. sdfibm replaces the traditional regularised Dirac delta function approach (Peskin's method) with the **Signed Distance Function (SDF)** φ(x), which stores the signed perpendicular distance from each fluid cell to the nearest solid surface. Cells with φ < 0 are inside the body; the body force is applied as a direct velocity correction in a narrow band around φ = 0:

```
φ(x) = ±dist(x, ∂s)
u*(x) = u_body ; where φ(x) ≤ 0
f(x) = (u_body − u_fluid) / Δt
```

This gives a sharp, geometry-consistent boundary without kernel tuning. The SDF is recomputed each timestep for moving bodies using a fast marching method, making it naturally suited to large-displacement motion such as flapping wings.

The solver is included as a Git submodule with custom motion types added for this project (Motion222000, MotionFlapping, etc.).

### Custom Motion Types

| Motion Type | Description | Parameters |
|---|---|---|
| `Motion222000` | Prescribed constant linear velocity (u, v, w), no rotation | `u`, `v`, `w` |
| `MotionFlapping` | Harmonic flapping — combined plunging and pitching | `plunging_amplitude`, `angular_amplitude` (deg), `period` |
| `Motion000002` | Constant Z-rotation, frozen translation | `period` |
| `MotionSineDirectional` | Sinusoidal oscillation along a prescribed direction | `amplitude`, `period`, `direction` |
| `Motion01Mask` | Generic 6-DOF constraint mask (0 = frozen, 1 = free) | `mask` (e.g., `b110001`) |

## Validation Cases

All cases use a fixed Cartesian mesh with the IBM body force applied as a source term in the momentum equation (PIMPLE algorithm, second-order backward time integration).

### 1. Cylinder (2D) — Re = 10

Flow past a cylinder with prescribed constant velocity `U = 0.01 m/s`. Validated against Goldstein's theoretical drag coefficient.

| Parameter | Value |
|---|---|
| Re | 10 |
| ν | 10⁻⁴ m²/s |
| U∞ | 0.01 m/s |
| Diameter | 0.1 m |
| Cells | 156,400 |
| Domain | 35D × 20D |
| Cd,sim | 3.01 |
| Cd,th | 3.06 |
| Error | 1.5% |

### 2. Sphere (3D) — Re = 10

Flow past a sphere with prescribed constant velocity `U = 0.01 m/s`. Validated against theoretical drag.

| Parameter | Value |
|---|---|
| Re | 10 |
| ν | 10⁻⁴ m²/s |
| U∞ | 0.01 m/s |
| Diameter | 0.1 m |
| Cells | 3,146,000 |
| Domain | 35D × 20D × 20D |
| Cd,sim | 4.16 |
| Cd,th | 4.15 |
| Error | 0.2% |

### 3. Flapping Plate (2D) — Re = 100

A rigid flat plate undergoing combined plunging and pitching (harmonic flapping). The motion is defined by:

```
x(t) = −h_a − h_a·cos(2π · t / T)    (plunging)
θ(t) = 90° − α_a·sin(2π · t / T)     (pitching)
```

| Parameter | Value |
|---|---|
| Re | 100 |
| ν | 10⁻⁴ m²/s |
| Uref | 0.1 m/s |
| Chord (D) | 0.1 m |
| Plunging amplitude (h_a) | 0.15 m |
| Angular amplitude (α_a) | 45° |
| Period (T) | 9.42 s |
| Cells | 500,000 |
| Domain | 6D × 3D |

## Repository Structure

```
.
├── sdfibm/                  # Git submodule — the SDF-IBM solver
│   └── src/
│       ├── libmotion/       # Custom motion types (MotionFlapping, etc.)
│       ├── libshape/        # Shape definitions using SDF (Circle, Rectangle, Sphere, etc.)
│       ├── libcollision/    # Collision detection
│       ├── libmaterial/     # Material properties
│       └── main.cpp         # Solver entry point (projection method + direct forcing)
├── cylinder/                # 2D flow past a cylinder (validation case)
│   ├── 0_org/               # Initial condition templates (p, U, T)
│   ├── constant/            # Transport properties, polyMesh
│   ├── system/              # controlDict, fvSolution, blockMeshDict, decomposeParDict
│   ├── solidDict            # IBM solid definition (circle, motion, material)
│   ├── Allrun               # Script to mesh, decompose, run, and post-process
│   ├── Allclean             # Script to clean the case
│   ├── plot_forces.py       # Drag coefficient plot
│   └── plot_residuals.py    # Residual convergence plot
├── sphere/                  # 3D flow past a sphere (validation case)
│   ├── (same structure as cylinder)
├── flapping_plate/          # 2D flapping flat plate (main validation case)
│   ├── (same structure as cylinder)
├── Poster.pdf               # Project poster presented at IIT Ropar
├── requirements.txt         # Python dependencies (matplotlib, numpy, scipy)
└── .devcontainer/           # VS Code devcontainer configuration (OpenFOAM 13)
    ├── Dockerfile           # Based on microfluidica/openfoam:13
    └── devcontainer.json
```

Each case directory follows the standard OpenFOAM case structure. The `solidDict` file (in `constant/`) defines the immersed body — its shape (Circle, Rectangle, Sphere), material properties, and prescribed motion. The `Allrun` script automates the entire workflow: meshing (`blockMesh`), decomposition (`decomposePar`), solving (`mpirun -np 8 ../sdfibm/build/src/sdfibm -parallel`), and post-processing (force/residual plots via Python).

## Setup

### Prerequisites

- OpenFOAM 13 (tested with [microfluidica/openfoam:13](https://hub.docker.com/r/microfluidica/openfoam) Docker image)
- A C++17 compiler (g++ ≥ 14.2.0 recommended)
- CMake
- Python 3 with matplotlib, numpy, scipy (see `requirements.txt`)
- ParaView (optional, for visualization)
- MPI (for parallel execution)

### Building sdfibm

```bash
git clone --recursive https://github.com/Nalin-Angrish/Bristled-Wing.git
cd Bristled-Wing/sdfibm
mkdir -p build && cd build
cmake ..
make -j$(nproc)
```

The compiled solver binary will be at `sdfibm/build/src/sdfibm`.

### Running a Case

```bash
cd cylinder   # or sphere, flapping_plate
./Allclean    # clean previous results
./Allrun      # mesh → decompose → solve → plot
```

The `Allrun` script:
1. Sources the OpenFOAM run functions
2. Runs `blockMesh` to generate the mesh
3. Copies initial conditions from `0_org/` to `0/`
4. Decomposes the domain with `decomposePar` (8 processors)
5. Runs `sdfibm` in parallel via MPI
6. Generates force-vs-time and residual plots

### VS Code Devcontainer

A `.devcontainer/` configuration is provided for a reproducible OpenFOAM 13 environment. Open the repository in VS Code and use "Reopen in Container" to build and attach to the Docker-based development environment.

## Output

The solver writes solid kinematics and forces to `cloud.out` (plain text). Each timestep produces one line per solid with columns:

```
t  x  y  z  vx  vy  vz  fx  fy  fz
```

In 2D, the columns are: `t  x  y  vx  vy  fx  fy  EulerAz  wz  Tz`

Visualization files (`.foam`) can be opened in ParaView for field inspection of velocity, pressure, and the IBM indicator field.

## References

1. Farisenkov et al. *Novel flight style and light wings boost flight performance of tiny beetles.* Nature, 602(7895):96–100, 2022.
2. Peskin. *The immersed boundary method.* Acta Numerica, 11:479–517, 2002.
3. Trizila et al. *Low-Reynolds-number aerodynamics of a flapping rigid flat plate.* AIAA Journal, 49(4):806–823, 2011.
4. Zhang et al. *Effective geometric algorithms for immersed boundary method using signed distance field.* Journal of Fluids Engineering, 141(6):061401, 2019.
5. Zhang. *sdfibm: a Signed Distance Field Based Discrete Forcing Immersed Boundary Method in OpenFOAM.* Computer Physics Communications, 2020.

## Credits

This project was conducted under the supervision of [Dr. Navaneeth K Marath](https://www.linkedin.com/in/navaneeth-k-marath-378337177/) at the [Department of Mechanical Engineering](https://www.linkedin.com/school/mechanical-engineering-iit-ropar/), [Indian Institute of Technology Ropar](https://www.iitrpr.ac.in/), as part of the First Capstone Project of:

- [Nalin Angrish](https://www.linkedin.com/in/nalin-angrish/) (2023MEB1360)
- [Eakamjit Singh](https://www.linkedin.com/in/eakamjit-singh/) (2023MEB1342)
- [Shubham Jhanga](https://www.linkedin.com/in/shubham-99b82828b/) (2023MEB1380)
