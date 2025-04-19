import numpy as np

class input_parameters:

   directory_BSE_geoopt                     = "./geoopt_BSE"

   directory_BSE_initial_single_point_calc  = "./init_single_point_BSE"

   CP2K_output_file_name                    = "cp2k.out"
   CP2K_output_file_name_initial_BSE        = ""

   excited_state_to_optimize                = 1

   
class BSE_init_parameters:

   struc = [
                ['O', (0.0, 0.0, 0.0)],
                ['H', (0.0, -0.757, 0.587)],
                ['H', (0.0,  0.757, 0.587)],
           ]

   E_GS = -1.0
   E_ES = -1.0

