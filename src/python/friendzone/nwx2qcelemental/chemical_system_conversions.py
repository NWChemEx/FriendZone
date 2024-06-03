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
from chemist import Molecule, Nuclei, Nucleus


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
        x = str(atom_i.x * au2ang)
        y = str(atom_i.y * au2ang)
        z = str(atom_i.z * au2ang)
        out += symbol + " " + x + " " + y + " " + z + "\n"
    return qcel.models.Molecule.from_data(out)


def qc_mol2molecule(qc_mol):
    """ Converts a QCElemental.Molecule object to a Chemist.Molecule object.


    .. note::

       QCElemental's Molecule class contains extra information that
       Chemist's Molecule class does not. At present this function ignores all
       extra information.

    """

    n_atoms = len(qc_mol.atom_labels)
    nuclei = Nuclei()
    mass_conversion = qcel.constants.conversion_factor("dalton", "au_mass")

    for i in range(n_atoms):
        sym = qc_mol.symbols[i]
        Zi = qc_mol.atomic_numbers[i]
        mass = qc_mol.masses[i] * mass_conversion
        x = qc_mol.geometry[i][0]
        y = qc_mol.geometry[i][1]
        z = qc_mol.geometry[i][2]
        nuclear_charge = float(Zi)
        nuclei.push_back(Nucleus(sym, Zi, mass, x, y, z, nuclear_charge))

    charge = int(qc_mol.molecular_charge)
    multiplicity = int(qc_mol.molecular_multiplicity)
    return Molecule(charge, multiplicity, nuclei)
