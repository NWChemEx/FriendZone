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

from friendzone.nwx2ase.chemical_system_conversions import chemical_system2atoms
from molecules import make_h2, make_h2o
from ase import Atoms
import unittest


def compare_ase(self, lhs, rhs):
    for lhs_Z, rhs_Z in zip(lhs.get_atomic_numbers(),
                            rhs.get_atomic_numbers()):
        self.assertEqual(lhs_Z, rhs_Z)

    for lhs_xyz, rhs_xyz in zip(lhs.get_positions(), rhs.get_positions()):
        for lhs_q, rhs_q in zip(lhs_xyz, rhs_xyz):
            self.assertAlmostEqual(lhs_q, rhs_q, places=4)

    for lhs_mass, rhs_mass in zip(lhs.get_masses(), rhs.get_masses()):
        self.assertAlmostEqual(lhs_mass, rhs_mass, places=4)


class TestChemicalSystemConversions(unittest.TestCase):

    def test_h2(self):
        corr_positions = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.8899966917653396)]
        corr = Atoms(numbers=(1, 1),
                     positions=corr_positions,
                     masses=[1.007825, 1.007825])

        h2_nwx = make_h2()
        ase_mol = chemical_system2atoms(h2_nwx)
        compare_ase(self, ase_mol, corr)

    def test_h2o(self):
        corr_positions = [(0.0, 0.7511511750790556, -0.46528276662873125),
                          (0.0, -0.7511511750790556, -0.46528276662873125),
                          (0.0, 0.0, 0.11632055936288019)]
        corr = Atoms(numbers=(1, 1, 8),
                     positions=corr_positions,
                     masses=[1.007825, 1.007825, 15.9990])

        h2o_nwx = make_h2o()
        ase_mol = chemical_system2atoms(h2o_nwx)
        compare_ase(self, ase_mol, corr)
