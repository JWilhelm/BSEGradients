import numpy as np
from Read_BSE_calcs import read_BSE_single_point_calc

def run_excited_state_geoopt(input_parameters):

  print("Input | Excited_state_to_optimize :", input_parameters.excited_state_to_optimize)

  # first BSE output: initial BSE calculation
  BSE_outputs = [read_BSE_single_point_calc(input_parameters)]

  print("test =", BSE_outputs[0].E_ES*27.211)

