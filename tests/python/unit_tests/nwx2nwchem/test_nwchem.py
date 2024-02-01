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

from pluginplay import ModuleManager
from friendzone import friends, load_modules
from simde import TotalEnergy
from molecules import make_h2
import unittest


class TestNWChem(unittest.TestCase):

    def test_scf(self):
        mol = make_h2()
        key = 'NWChem : SCF'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        self.assertAlmostEqual(egy, -1.094184522864, places=5)

    def test_mp2(self):
        mol = make_h2()
        key = 'NWChem : MP2'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        self.assertAlmostEqual(egy, -1.111247857166, places=5)

    def test_ccsd(self):
        mol = make_h2()
        key = 'NWChem : CCSD'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        self.assertAlmostEqual(egy, -1.122251361965036, places=4)

    def test_ccsd_t(self):
        mol = make_h2()
        key = 'NWChem : CCSD(T)'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        self.assertAlmostEqual(egy, -1.122251361965036, places=4)

    def setUp(self):
        if not friends.is_friend_enabled('nwchem'):
            self.skipTest("NWChem backend is not enabled!")

        self.mm = ModuleManager()
        load_modules(self.mm)
