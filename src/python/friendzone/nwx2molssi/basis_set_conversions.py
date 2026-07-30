# Copyright 2026 NWChemEx-Project
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

from chemist import PointD, ShellType
from chemist.basis_set import AOBasisSetD, AtomicBasisSetD, ShellD


def qc_basis2ao_basis_set(qc_mol, qc_basis):
    """Converts a QCElemental inline BasisSet into a Chemist AOBasisSetD.

    :param qc_mol: The molecule the basis set is defined for. Used to map
                   each atom to its center data (via ``qc_basis.atom_map``)
                   and to its Cartesian coordinates.
    :type qc_mol: qcelemental.models.Molecule
    :param qc_basis: The inline basis set description to convert. A basis
                     set specified only by name (a bare string) is not
                     supported by this function; resolve it to an inline
                     ``qcelemental.models.basis.BasisSet`` first (e.g. via a
                     basis-set library) before calling this function.
    :type qc_basis: qcelemental.models.basis.BasisSet

    :return: The Chemist representation of ``qc_basis``.
    :rtype: chemist.basis_set.AOBasisSetD
    """

    aos = AOBasisSetD()
    n_atoms = len(qc_mol.symbols)

    for i in range(n_atoms):
        center_key = qc_basis.atom_map[i]
        center = qc_basis.center_data[center_key]
        x, y, z = qc_mol.geometry[i]

        shells = []
        for electron_shell in center.electron_shells:
            if len(electron_shell.angular_momentum) != 1:
                raise NotImplementedError(
                    "Shells sharing multiple angular momenta (e.g. SP "
                    "shells) are not supported"
                )
            l = electron_shell.angular_momentum[0]
            pure = (
                ShellType.pure
                if electron_shell.harmonic_type == "spherical"
                else ShellType.cartesian
            )
            exponents = electron_shell.exponents
            # Each row of ``coefficients`` is a separate (segmented)
            # contraction sharing the same exponents; Chemist's Shell only
            # holds a single set of coefficients, so a general contraction
            # becomes one Shell per row.
            for coefficients in electron_shell.coefficients:
                shells.append(ShellD(pure, l, coefficients, exponents, x, y, z))

        center = PointD(x, y, z)
        atomic_basis_set = AtomicBasisSetD(
            qc_basis.name, qc_mol.atomic_numbers[i], center, shells
        )
        aos.add_center(atomic_basis_set)

    return aos
