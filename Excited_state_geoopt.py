import numpy as np
from Read_BSE_calcs import read_BSE_initial_single_point_calc

def run_excited_state_geoopt(input_parameters):

  print("Input | Excited_state_to_optimize :", input_parameters.excited_state_to_optimize)

  BSE_init = read_BSE_initial_single_point_calc(input_parameters)
