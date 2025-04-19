import numpy as np

class INPUT_PARAMETERS:

   directory_BSE_geoopt                     = "./geoopt_BSE"

   directory_BSE_initial_single_point_calc  = "./init_single_point_BSE"

   CP2K_output_file_name                    = "cp2k.out"

   BSE_input_file_name                      = "BSE.inp"

   excited_state_to_optimize                = 1

   atom_displacement_in_Angstrom            = 0.01

   threshold_energy_change_eV               = 0.001


class CONTROL_PARAMETERS:

   BSE_gradient_index                       = 0

   BSE_single_point_index                   = 0


class BSE_OUTPUT:

   struc = [
                ['A', (0.0, 0.1, 0.2)],
                ['B', (0.3, 0.4, 0.5)],
                ['C', (0.6, 0.7, 0.8)],
           ]

   coords_array = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

   E_GS  = -1.0
   E_ES  = -1.0
   E_tot = -1.0

class CONSTANTS:

   eV = 27.211


