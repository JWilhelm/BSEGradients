from Parameters import BSE_init_parameters
import os

def read_BSE_initial_single_point_calc(input_parameters):

   BSE_init = BSE_init_parameters()

   input_parameters.CP2K_output_file_name_initial_BSE = os.path.join(\
                    input_parameters.directory_BSE_initial_single_point_calc, \
                    input_parameters.CP2K_output_file_name)

   BSE_init_parameters.struc = read_cp2k_coord(input_parameters.CP2K_output_file_name_initial_BSE)

   return BSE_init

def read_cp2k_coord(filename):

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    struc = []

    # Try UTF-8 first, fallback to Latin-1 if decoding fails
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as f:
            lines = f.readlines()

    # Find the header line indicating the start of coordinates
    start_idx = None
    for i, line in enumerate(lines):
        if "MODULE QUICKSTEP: ATOMIC COORDINATES IN ANGSTROM" in line:
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("Could not find atomic coordinates section in the file.")

    # Skip two lines (header + column names)
    coord_lines = lines[start_idx + 3:]

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

    print("Molecular geometry: Atom type, x, y, z (in Angström)")
    for elem, coords in struc:
        print(f"    {elem}   {coords[0]:.6f}   {coords[1]:.6f}   {coords[2]:.6f}")

    return struc
