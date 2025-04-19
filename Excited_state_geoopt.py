import numpy as np
import os
from scipy.optimize import minimize
from BSE_calc_read  import  read_BSE_single_point_calc
from BSE_calc_start import start_BSE_single_point_calc, calcdirname
from Parameters import CONTROL_PARAMETERS, CONSTANTS

def run_excited_state_geoopt(input_parameters):

  print("Input | Excited_state_to_optimize :", input_parameters.excited_state_to_optimize)

  # first BSE output: initial BSE calculation
  BSE_output_init = read_BSE_single_point_calc(input_parameters, 
                                 input_parameters.directory_BSE_initial_single_point_calc)

  control_parameters = CONTROL_PARAMETERS()

  os.mkdir(input_parameters.directory_BSE_geoopt)

  BFGS_result = minimize(
      fun=energy_function,
      x0=BSE_output_init.coords_array,
      jac=gradient_function,
      args=(input_parameters,control_parameters,),
      method='BFGS',
      tol=input_parameters.threshold_energy_change_eV,
      options={'disp': True, 'maxiter': 50}
  )

  print(f"\nFinal energy: {BFGS_result.fun:.8f} Hartree ({BFGS_result.fun*CONSTANTS.eV:.3f} eV)")

  # Print final geometry
  final_coords = BFGS_result.x.reshape((-1, 3))
  print("\nFinal coordinates (Angstrom):")
  for i, (x, y, z) in enumerate(final_coords):
      print(f"Atom {i+1}: {x:.6f} {y:.6f} {z:.6f}")

def energy_function(coords_array, input_parameters, control_parameters):

    control_parameters.BSE_gradient_index += 1
    control_parameters.BSE_single_point_index = 0

    start_BSE_single_point_calc(input_parameters, control_parameters, coords_array)

    calcdir = calcdirname(control_parameters, input_parameters)
    BSE_output = read_BSE_single_point_calc(input_parameters, calcdir)

    energy = BSE_output.E_tot

    return energy

def gradient_function(coords_array, input_parameters, control_parameters):

    control_parameters.BSE_gradient_index += 1
    control_parameters.BSE_single_point_index = 0

    n_atoms = len(coords_array) // 3
    grad = np.zeros_like(coords_array)
    delta = input_parameters.atom_displacement_in_Angstrom

    for i in range(len(coords_array)):
        coords_array_forward = coords_array.copy()
        coords_array_backward = coords_array.copy()
        coords_array_forward[i] += delta
        coords_array_backward[i] -= delta

        start_BSE_single_point_calc(input_parameters, control_parameters, coords_array_forward)
        start_BSE_single_point_calc(input_parameters, control_parameters, coords_array_backward)


    control_parameters.BSE_single_point_index = 0

    for i in range(len(coords_array)):

        control_parameters.BSE_single_point_index += 1
        calcdir = calcdirname(control_parameters, input_parameters)
        BSE_output_1 = read_BSE_single_point_calc(input_parameters, calcdir)
        E_plus = BSE_output_1.E_tot

        control_parameters.BSE_single_point_index += 1
        calcdir = calcdirname(control_parameters, input_parameters)
        BSE_output_2 = read_BSE_single_point_calc(input_parameters, calcdir)
        E_minus = BSE_output_2.E_tot

        if BSE_output_1.BSE_success and BSE_output_2.BSE_success:
           grad[i] = (E_plus - E_minus) / (2 * delta)
        else:
           grad[i] = 0.0

    return grad

