# Basic Airfoil Example
This is a basic example to simulate the flow over an airfoil using OpenFOAM. The airfoil geometry is generated using Gmsh, and the simulation is set up to analyze the aerodynamic properties of the airfoil.

## Mesh Generation
To generate the mesh for the airfoil, run the `genMesh` script:
```sh 
./genMesh
```
This will prompt you for the airfoil (a NACA 4-digit code) and create the mesh accordingly.

Configuration for the mesh can be done in the `configuration.geo` file, where you can set parameters for mesh refinement and domain size.

## Running the Simulation
Set the velocity and the angle of attack in the `0/variables/data` file before running the simulation. Other properties do not matter but can be adjusted as needed.

After generating the mesh, you can run the simulation using the following command:
```sh 
./runSim
```

## Post-Processing
After the simulation is complete, you can visualize the results using ParaView or any other compatible post-processing tool. You can analyze the flow characteristics around the airfoil, including pressure distribution and velocity fields.

The lift and drag coefficients are calculated and can be found in the `postProcessing/forceCoeffs/0/forceCoeffs.dat` file.

## Optimizations
Certain decisions were observed to optimize the simulation:
- Use multiprocessing to speed up the simulation.  
- Don't print the log output to the console; instead, redirect it to a file for better performance.

These optimizations may be considered for future components of the project.

## Cleaning Up
To clean up the generated files, you can run:
```sh 
./clean
```