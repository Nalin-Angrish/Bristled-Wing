# CFD-Based Modeling of Bristled Wings in Low Reynolds Number Regimes
This repository contains the code and resources for the project titled "CFD-Based Modeling of Bristled Wings in Low Reynolds Number Regimes". The project focuses on simulating aerodynamic performance of bristled wings using the Immersed Boundary Method.

## Setup
To set up the environment for running the simulations, ensure you have [Foam Extend](https://sourceforge.net/projects/foam-extend/), [ParaView](https://www.paraview.org/) and [Gmsh](https://gmsh.info/) installed on your system. Follow the instructions in the respective documentation for installation. For certain scripts, Python 3 is also required. There are also other shell scripts provided to automate various tasks which would require a Unix-like environment. Our team has been using Ubuntu 24.04 LTS (either as a complete install or inside WSL) for development and testing.

We are using `foam-extend-5.0` instead of the latest OpenFOAM version due to its inbuilt solver for the Immersed Boundary Method, which is crucial for our simulations. The specific version of `foam-extend` can be installed from the [SourceForge page](https://sourceforge.net/projects/foam-extend/files/foam-extend-5.0/). Please follow the installation instructions provided in the documentation to set up `foam-extend-5.0` correctly.

## Components
- **AirfoilBasic**: A basic example to simulate the flow over an airfoil using OpenFOAM. ATP this probably doesn't work correctly, and will be updated soon.
- **cylinder_conv**: A basic example to simulate the flow over a cylinder using OpenFOAM's SIMPLE solver. This has been validated with literature and serves as a benchmark case for our simulations.
- **cylinder_ibm**: A basic example to simulate the flow over a cylinder using the Immersed Boundary Method in `foam-extend-5.0`. This will be our first test case to validate the IBM implementation before applying it to more complex geometries like bristled wings.

Detailed descriptions and instructions for all components can be found in their respective directories' README files. More components will be added soon as the project progresses.

## Credits
This project was done under the supervision of [Dr. Navaneeth K Marath](https://www.linkedin.com/in/navaneeth-k-marath-378337177/) at the [Department of Mechanical Engineering](https://www.linkedin.com/school/mechanical-engineering-iit-ropar/), [Indian Institute of Technology Ropar](https://www.iitrpr.ac.in/), as a part of the First Capstone Project of:
- [Nalin Angrish](https://www.linkedin.com/in/nalin-angrish/) (2023MEB1360)
- [Eakamjit Singh](https://www.linkedin.com/in/eakamjit-singh/) (2023MEB1342)
- [Shubham Jhanga](https://www.linkedin.com/in/shubham-99b82828b/) (2023MEB1380)