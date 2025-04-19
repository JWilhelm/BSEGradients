import numpy as np
import os
from scipy.optimize import minimize
from BSE_calc_read  import  read_BSE_single_point_calc
from BSE_calc_start import start_BSE_single_point_calc
from Parameters import CONTROL_PARAMETERS

def run_excited_state_geoopt(input_parameters):

  print("Input | Excited_state_to_optimize :", input_parameters.excited_state_to_optimize)

  # first BSE output: initial BSE calculation
  BSE_output_init = read_BSE_single_point_calc(input_parameters)

  print("test =", BSE_output_init.E_ES*27.211)

  control_parameters = CONTROL_PARAMETERS()

  os.mkdir(input_parameters.directory_BSE_geoopt)

  BFGS_result = minimize(
      fun=energy_function,
      x0=BSE_output_init.coord_array,
      jac=gradient_function,
      args=(input_parameters,control_parameters,),
      method='BFGS',
      tol=input_parameters.threshold_energy_change_eV,
      options={'disp': True, 'maxiter': 50}
  )


def energy_function(coords_array, input_parameters, control_parameters):

    control_parameters.BSE_single_point_index += 1

    print("INDEX = ", control_parameters.BSE_single_point_index)

    start_BSE_single_point_calc(input_parameters, control_parameters, coords_array)

    energy = 0.2
    return energy

def gradient_function(coords_array, input_parameters, control_parameters):

    control_parameters.BSE_gradient_index += 1

    n_atoms = len(coords_array) // 3
    grad = np.zeros_like(coords_array)
    delta = input_parameters.atom_displacement_in_Angstrom

    for i in range(len(coords_array)):
        coords_array_forward = coords_array.copy()
        coords_array_backward = coords_array.copy()
        coords_array_forward[i] += delta
        coords_array_backward[i] -= delta

#        input_parameters.set_geometry(coords_array_forward.reshape((n_atoms, 3)))
#        E_plus = read_BSE_single_point_calc(input_parameters).E_ES
#
#        input_parameters.set_geometry(coords_array_backward.reshape((n_atoms, 3)))
#        E_minus = read_BSE_single_point_calc(input_parameters).E_ES
#
#        grad[i] = (E_plus - E_minus) / (2 * delta)

        grad[i] = 0.1

    return grad

