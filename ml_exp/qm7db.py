"""MIT License

Copyright (c) 2019 David Luevano Alvarado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import numpy as np
import random


# 'hof_qm7.txt.txt' retrieved from
# https://github.com/qmlcode/tutorial
def qm7db(nc,
          db_path='data',
          r_seed=111):
    """
    Creates a list of compounds with the qm7 database.
    nc: dictionary containing nuclear charge data.
    db_path: path to the database directory.
    r_seed: random seed to use for the shuffling.
    """

    fname = f'{db_path}/hof_qm7.txt'
    with open(fname, 'r') as f:
        lines = f.readlines()

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
    atoms = []
    # Actual reading of the xyz files.
    for i, k in enumerate(energy_temp_shuffled.keys()):
        with open(k, 'r') as xyz_file:
            lines = xyz_file.readlines()

        len_lines = len(lines)
        mol_temp_data = []
        mol_nc_temp_data = np.array(np.zeros(len_lines-2))
        atoms_temp = []
        for j, line in enumerate(lines[2:len_lines]):
            line_list = line.split()

            atoms_temp.append(line_list[0])
            mol_nc_temp_data[j] = float(nc[line_list[0]])
            line_data = np.array(np.asarray(line_list[1:4], dtype=float))
            mol_temp_data.append(line_data)

        mol_data.append(mol_temp_data)
        mol_nc_data.append(mol_nc_temp_data)
        atoms.append(atoms_temp)

    # Convert everything to a numpy array.
    molecules = np.array([np.array(mol) for mol in mol_data])
    nuclear_charge = np.array([nc_d for nc_d in mol_nc_data])
    energy_pbe0 = np.array([energy_temp_shuffled[k][0]
                            for k in energy_temp_shuffled.keys()])
    energy_delta = np.array([energy_temp_shuffled[k][1]
                             for k in energy_temp_shuffled.keys()])

    return molecules, nuclear_charge, energy_pbe0, energy_delta, atoms
