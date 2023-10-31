# Copyright 2023 NWChemEx-Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import qcelemental as qcel

def chemical_system2qc_mol(chem_sys):
    """ Converts a chemist.ChemicalSystem object into a QCElemental.Molecule

    At present there is far more information in the input chemical system
    then in the output object. In particular, our implementation only
    worries about:

    - Chemical symbols
    - Cartesian coordinates (including the Bohr to angstrom conversion)

    :param chem_sys: The NWChemEx description of the chemical system we want to
                     convert.
    :type chem_sys: chemist.ChemicalSystem
    :return: The QCElemental representation of ``chem_sys``
    :rtype: qcelemental.models.Molecule
    """

    out = ""
    mol = chem_sys.molecule
    au2ang = qcel.constants.conversion_factor("bohr", "angstrom")
    for i in range(mol.size()):
        atom_i = mol.at(i)
        symbol = atom_i.name
        x      = str(atom_i.x * au2ang)
        y      = str(atom_i.y * au2ang)
        z      = str(atom_i.z * au2ang)
        out += symbol + " " + x + " " + y + " " + z + "\n"
    return qcel.models.Molecule.from_data(out)
