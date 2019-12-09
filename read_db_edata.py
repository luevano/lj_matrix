import os
import numpy as np
import random


# 'hof_qm7.txt.txt' retrieved from
# https://github.com/qmlcode/tutorial
def read_db_edata(zi_data,
                  data_path,
                  r_seed=111):
    """
    Reads molecule database and extracts
    its contents as usable variables.
    zi_data: dictionary containing nuclear charge data.
    data_path: path to the data directory.
    r_seed: random seed.
    """
    os.chdir(data_path)

    fname = 'hof_qm7.txt'
    with open(fname, 'r') as infile:
        lines = infile.readlines()

    # Temporary energy dictionary.
    energy_temp = dict()

    for line in lines:
        xyz_data = line.split()

        xyz_name = xyz_data[0]
        hof = float(xyz_data[1])
        dftb = float(xyz_data[2])
        # print(xyz_name, hof, dftb)

        energy_temp[xyz_name] = np.array([hof, hof - dftb])

    # Use a random seed.
    random.seed(r_seed)

    et_keys = list(energy_temp.keys())
    random.shuffle(et_keys)

    # Temporary energy dictionary, shuffled.
    energy_temp_shuffled = dict()
    for key in et_keys:
        energy_temp_shuffled.update({key: energy_temp[key]})

    mol_data = []
    mol_nc_data = []
    # Actual reading of the xyz files.
    for i, k in enumerate(energy_temp_shuffled.keys()):
        with open(k, 'r') as xyz_file:
            lines = xyz_file.readlines()

        len_lines = len(lines)
        mol_temp_data = []
        mol_nc_temp_data = np.array(np.zeros(len_lines-2))
        for j, line in enumerate(lines[2:len_lines]):
            line_list = line.split()

            mol_nc_temp_data[j] = float(zi_data[line_list[0]])
            line_data = np.array(np.asarray(line_list[1:4], dtype=float))
            mol_temp_data.append(line_data)

        mol_data.append(mol_temp_data)
        mol_nc_data.append(mol_nc_temp_data)

    # Convert everything to a numpy array.
    molecules = np.array([np.array(mol) for mol in mol_data])
    nuclear_charge = np.array([nc_d for nc_d in mol_nc_data])
    energy_pbe0 = np.array([energy_temp_shuffled[k][0]
                            for k in energy_temp_shuffled.keys()])
    energy_delta = np.array([energy_temp_shuffled[k][1]
                             for k in energy_temp_shuffled.keys()])

    return molecules, nuclear_charge, energy_pbe0, energy_delta
