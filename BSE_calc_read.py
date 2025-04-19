from Parameters import BSE_OUTPUT, CONSTANTS
import os
import time
import math

def read_BSE_single_point_calc(input_parameters, calcdir):

   BSE_output_1 = BSE_OUTPUT()

   cp2k_out = os.path.join(calcdir, input_parameters.CP2K_output_file_name)

   # Wait until file exists
   while not os.path.isfile(cp2k_out):
       time.sleep(1)
   
   # Wait until "T I M I N G" appears in the file (appears once CP2K finished successfully)
   while True:
       try:
           with open(cp2k_out, 'r', encoding='utf-8') as f:
               contents = f.read()
       except UnicodeDecodeError:
           with open(cp2k_out, 'r', encoding='latin-1') as f:
               contents = f.read()
   
       if "T I M I N G" in contents:
           BSE_success = True
           break

       if "ABORT" in contents:
           BSE_success = False
           break
   
       time.sleep(1)

#   if not os.path.isfile(cp2k_out):
#       raise FileNotFoundError(f"File '{cp2k_out}' does not exist.")

   # Try UTF-8 first, fallback to Latin-1 if decoding fails
   try:
       with open(cp2k_out, 'r', encoding='utf-8') as f:
           lines = f.readlines()
   except UnicodeDecodeError:
       with open(cp2k_out, 'r', encoding='latin-1') as f:
           lines = f.readlines()

   # Find the header line indicating the start of coordinates
   start_idx_struc = -1000
   start_idx_BSE_ABBA = -1000
   for i, line in enumerate(lines):
       if "Total energy:" in line:
           parts = line.strip().split()
           try:
               E_GS = float(parts[-1])
           except ValueError:
               print("Error when reading total E_GS")
               continue  # Malformed E_GS line, skip

       if "MODULE QUICKSTEP: ATOMIC COORDINATES IN ANGSTROM" in line:
           start_idx_struc = i
       if "Excitation energies from solving the BSE without the TDA:" in line:
           start_idx_BSE_ABBA = i
       if i == start_idx_BSE_ABBA + 2 + input_parameters.excited_state_to_optimize:
           parts = line.strip().split()
           E_ES = float(parts[-1]) / CONSTANTS.eV

   if start_idx_struc is None:
       raise ValueError("Could not find atomic coordinates section in the file.")

   # Skip two lines (header + column names)
   coord_lines  = lines[start_idx_struc + 3:]
   struc        = []
   coords_array = []

   for line in coord_lines:
       line = line.strip()
       if not line:
           break  # Stop at the first empty line after coordinate block
       parts = line.split()
       if len(parts) < 8:
           continue  # Skip malformed lines
       element = parts[2]
       x, y, z = map(float, parts[4:7])
       struc.append([element, (x, y, z)])
       coords_array.extend([x, y, z])

   if not BSE_success:
       # 
       E_ES = 0.6

   print("\nMolecular geometry: Atom type, x, y, z (in Angström)")
   for elem, coords in struc:
       print(f"                    {elem}   {coords[0]:.6f}   {coords[1]:.6f}   {coords[2]:.6f}")
   print(f"\nGround state energy: {E_GS:.8f} Hartree ({E_GS*CONSTANTS.eV:.4f} eV)")
   print(f"\nExcited state energy: {E_ES:.8f} Hartree ({E_ES*CONSTANTS.eV:.4f} eV)")
   print(f"\nTotal energy:        {E_ES+E_GS:.8f} Hartree ({(E_ES+E_GS)*CONSTANTS.eV:.4f} eV)")
   print(f"\n")

   BSE_output_1.struc        = struc
   BSE_output_1.coords_array = coords_array
   BSE_output_1.E_GS         = E_GS
   BSE_output_1.E_ES         = E_ES
   BSE_output_1.E_tot        = E_GS + E_ES
   BSE_output_1.BSE_success  = BSE_success

   return BSE_output_1
