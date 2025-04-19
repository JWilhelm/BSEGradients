import numpy as np

class INPUT_PARAMETERS:

   directory_BSE_geoopt                     = "./geoopt_BSE"

   directory_BSE_initial_single_point_calc  = "./init_single_point_BSE"

   CP2K_output_file_name                    = "cp2k.out"

   excited_state_to_optimize                = 1

   atom_displacement_in_Bohr                = 0.01

   
class BSE_OUTPUT:

   struc = [
                ['A', (0.0, 0.0, 0.0)],
                ['B', (0.0, 0.0, 0.0)],
                ['C', (0.0, 0.0, 0.0)],
           ]

   E_GS  = -1.0
   E_ES  = -1.0
   E_tot = -1.0

class CONSTANTS:

   eV = 27.211


