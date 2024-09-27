# Copyright 2024 NWChemEx-Project
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

from ase import Atoms, units


def chemical_system2atoms(chem_sys):
    """Converts a chemist.ChemicalSystem object into an ASE Atoms object."""

    atomic_numbers = []
    positions = []
    masses = []
    au2ang = units.Bohr
    me2amu = units._me * units.kg

    for atom in chem_sys.molecule:
        atomic_numbers.append(atom.Z)
        masses.append(atom.mass * me2amu)
        x = atom.x * au2ang
        y = atom.y * au2ang
        z = atom.z * au2ang
        positions.append((x, y, z))

    return Atoms(numbers=atomic_numbers, positions=positions, masses=masses)
