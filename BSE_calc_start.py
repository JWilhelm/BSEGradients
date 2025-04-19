from Parameters import BSE_OUTPUT, CONSTANTS
import os
import shutil
import subprocess

def start_BSE_single_point_calc(input_parameters, control_parameters, coords_array):

   control_parameters.BSE_single_point_index += 1

   calcdir = calcdirname(control_parameters, input_parameters)
 
   shutil.copytree(input_parameters.directory_BSE_initial_single_point_calc, calcdir)

   os.chdir(calcdir)

   for filename in os.listdir('.'):
       if ("RESTART" in filename or "out" in filename or "ABBA" in filename) \
           and os.path.isfile(filename):
           os.remove(filename)

   write_new_coords_to_input(input_parameters, coords_array)

   subprocess.run(["sbatch", "run.sh"], check=True, stdout=subprocess.DEVNULL, \
                  stderr=subprocess.DEVNULL)

   os.chdir("../..")


def write_new_coords_to_input(input_parameters, coords_array):

   with open(input_parameters.BSE_input_file_name, 'r') as f:
       lines = f.readlines()
   
   new_lines = []
   inside_coord = False
   atom_index = 0
   
   for line in lines:
       if "&COORD" in line:
           inside_coord = True
           new_lines.append(line)
           continue
       if "&END COORD" in line:
           inside_coord = False
           new_lines.append(line)
           continue
   
       if inside_coord:
           parts = line.strip().split()
           atom_type = parts[0]
           x = coords_array[atom_index * 3 + 0] 
           y = coords_array[atom_index * 3 + 1]
           z = coords_array[atom_index * 3 + 2]
           new_lines.append(f"   {atom_type}  {x:.6f}  {y:.6f}  {z:.6f}\n")
           atom_index += 1
       else:
           new_lines.append(line)
   
   # overwrite the input file
   with open(input_parameters.BSE_input_file_name, "w") as f:
       f.writelines(new_lines)


def calcdirname(control_parameters, input_parameters):
   calcdir = f"Grad_{control_parameters.BSE_gradient_index:03d}_single_point_{control_parameters.BSE_single_point_index:06d}"

   calcdir = os.path.join(input_parameters.directory_BSE_geoopt, calcdir)

   return calcdir
