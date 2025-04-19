from Parameters import BSE_OUTPUT
import os

def read_BSE_initial_single_point_calc(INPUT_PARAMETERS):

   BSE_output_1 = BSE_OUTPUT()

   cp2k_out = os.path.join(INPUT_PARAMETERS.directory_BSE_initial_single_point_calc, \
                           INPUT_PARAMETERS.CP2K_output_file_name)

   if not os.path.isfile(cp2k_out):
       raise FileNotFoundError(f"File '{cp2k_out}' does not exist.")

   struc = []

   # Try UTF-8 first, fallback to Latin-1 if decoding fails
   try:
       with open(cp2k_out, 'r', encoding='utf-8') as f:
           lines = f.readlines()
   except UnicodeDecodeError:
       with open(cp2k_out, 'r', encoding='latin-1') as f:
           lines = f.readlines()

   # Find the header line indicating the start of coordinates
   start_idx_struc = None
   for i, line in enumerate(lines):
       if "Total energy:" in line:
           parts = line.strip().split()
           try:
               energy = float(parts[-1])
           except ValueError:
               print("Error when reading total energy")
               continue  # Malformed energy line, skip

       if "MODULE QUICKSTEP: ATOMIC COORDINATES IN ANGSTROM" in line:
           start_idx_struc = i

   if start_idx_struc is None:
       raise ValueError("Could not find atomic coordinates section in the file.")

   # Skip two lines (header + column names)
   coord_lines = lines[start_idx_struc + 3:]

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

   print("\nMolecular geometry: Atom type, x, y, z (in Angström)")
   for elem, coords in struc:
       print(f"                    {elem}   {coords[0]:.6f}   {coords[1]:.6f}   {coords[2]:.6f}")
   print(f"\nGround state energy: {energy} Hartree")


   BSE_output_1.struc  = struc
   BSE_output_1.energy = energy

   return BSE_output_1
