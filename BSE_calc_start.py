from Parameters import BSE_OUTPUT, CONSTANTS
import os
import shutil

def start_BSE_single_point_calc(input_parameters, control_parameters, coords_array):

   calcdir = f"Grad_{control_parameters.BSE_gradient_index:03d}_single_point_{control_parameters.BSE_single_point_index:06d}"

   calcdirpath = os.path.join(input_parameters.directory_BSE_geoopt, calcdir)

   shutil.copytree(input_parameters.directory_BSE_initial_single_point_calc, calcdirpath)

   os.chdir(calcdirpath)

   for filename in os.listdir('.'):
       if ("RESTART" in filename or "out" in filename or "ABBA" in filename) \
           and os.path.isfile(filename):
           os.remove(filename)

   os.chdir("../..")
