// Gmsh project created on Sun Jan 25 18:20:51 2026
Include "airfoil.geo";
Include "configuration.geo";

//+
Point(200) = {-0.5, ymax, 0, 1.0};
//+
Point(201) = {-0.5, -ymax, 0, 1.0};
//+
Point(202) = {1, -ymax, 0, 1.0};
//+
Point(203) = {1, ymax, 0, 1.0};
//+
Point(204) = {xmax, ymax, 0, 1.0};
//+
Point(205) = {xmax, -ymax, 0, 1.0};
//+
Point(206) = {xmax, 0, 0, 1.0};
//+
Circle(2) = {200, 100, 201};
//+
Line(3) = {200, 90};
//+
Line(4) = {201, 110};
//+
Line(5) = {200, 203};
//+
Line(6) = {201, 202};
//+
Line(7) = {203, 204};
//+
Line(8) = {202, 205};
//+
Line(9) = {206, 205};
//+
Line(10) = {206, 204};
//+
Line(11) = {1, 203};
//+
Line(12) = {1, 202};
//+
Line(13) = {1, 206};
//+
Split Curve {1} Point {90, 110};
//+
Split Curve {15} Point {1};
//+
Transfinite Curve {2, 14} = n_inlet Using Progression 1;
//+
Transfinite Curve {3, 11} = n_vertical Using Progression 1/r_vertical;
Transfinite Curve {11, 10} = n_vertical Using Progression r_vertical;
//+
Transfinite Curve {4, 12} = n_vertical Using Progression 1/r_vertical;
Transfinite Curve {12, 9} = n_vertical Using Progression r_vertical;
//+
Transfinite Curve {17, 5} = n_airfoil Using Bump 0.7;
Transfinite Curve {16, 6} = n_airfoil Using Bump 0.7;
//+
Transfinite Curve {7, 13, 8} = n_wake Using Progression r_wake;
//+
Curve Loop(1) = {2, 4, -14, -3};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, -17, 11, -5};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {4, 16, 12, -6};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {11, 7, -10, -13};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, 8, -9, -13};
//+
Plane Surface(5) = {5};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {3};
//+
Recombine Surface {1, 2, 4, 5, 3};
//+
Extrude {0, 0, 0.1} {
  Surface{1}; Surface{2}; Surface{4}; Surface{5}; Surface{3}; Layers {1}; Recombine;
}
//+
Physical Volume("fluid", 128) = {1, 2, 3, 4, 5};
//+
Physical Surface("inlet", 129) = {26, 60, 74, 126, 96};
//+
Physical Surface("outlet", 130) = {78, 100};
//+
Physical Surface("airfoil", 131) = {52, 34, 118};
//+
Physical Surface("side", 132) = {39, 61, 83, 127, 105, 1, 2, 3, 5, 4};
