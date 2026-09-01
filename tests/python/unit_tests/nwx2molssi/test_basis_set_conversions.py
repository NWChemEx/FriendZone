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

import unittest

from friendzone.friends import is_molssi_enabled

if is_molssi_enabled():
    import qcelemental as qcel
    from chemist import PointD, ShellType
    from chemist.basis_set import AOBasisSetD, AtomicBasisSetD, ShellD
    from friendzone.nwx2molssi.basis_set_conversions import (
        qc_basis2ao_basis_set,
    )


class TestQCBasis2AOBasisSet(unittest.TestCase):
    def test_h2(self):
        result = qc_basis2ao_basis_set(self.qc_mol, self.qc_basis)

        corr = AOBasisSetD()
        for coords in [(0.0, 0.0, 0.0), (0.0, 0.0, 1.68185)]:
            shell = ShellD(ShellType.cartesian, 0, [1.0], [0.5], *coords)
            center = PointD(*coords)
            abs_ = AtomicBasisSetD("test-basis", 1, center, [shell])
            corr.add_center(abs_)

        self.assertEqual(result, corr)

    def test_general_contraction_expands_to_multiple_shells(self):
        shell = qcel.models.v2.ElectronShell(
            angular_momentum=[0],
            harmonic_type="cartesian",
            exponents=[0.5],
            coefficients=[[1.0], [2.0]],
        )
        center = qcel.models.v2.BasisCenter(electron_shells=[shell])
        basis = qcel.models.v2.BasisSet(
            name="test-basis", center_data={"h": center}, atom_map=["h", "h"]
        )

        result = qc_basis2ao_basis_set(self.qc_mol, basis)
        self.assertEqual(result.n_shells(), 4)

    def test_multiple_angular_momenta_not_supported(self):
        shell = qcel.models.v2.ElectronShell(
            angular_momentum=[0, 1],
            harmonic_type="cartesian",
            exponents=[0.5],
            coefficients=[[1.0], [1.0]],
        )
        center = qcel.models.v2.BasisCenter(electron_shells=[shell])
        basis = qcel.models.v2.BasisSet(
            name="test-basis", center_data={"h": center}, atom_map=["h", "h"]
        )

        with self.assertRaises(NotImplementedError):
            qc_basis2ao_basis_set(self.qc_mol, basis)

    def setUp(self):
        if not is_molssi_enabled():
            self.skipTest("MolSSI friend is not enabled!")

        h2_as_str = "units a.u.\nH 0.0 0.0 0.0\nH 0.0 0.0 1.68185"
        self.qc_mol = qcel.models.v2.Molecule.from_data(h2_as_str)

        shell = qcel.models.v2.ElectronShell(
            angular_momentum=[0],
            harmonic_type="cartesian",
            exponents=[0.5],
            coefficients=[[1.0]],
        )
        center = qcel.models.v2.BasisCenter(electron_shells=[shell])
        self.qc_basis = qcel.models.v2.BasisSet(
            name="test-basis", center_data={"h": center}, atom_map=["h", "h"]
        )
