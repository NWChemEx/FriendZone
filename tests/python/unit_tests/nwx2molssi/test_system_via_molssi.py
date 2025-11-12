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

import unittest

from compare_molecules import compare_molecules
from friendzone import load_modules
from friendzone.friends import is_molssi_enabled
from molecules import make_h2
from pluginplay import ModuleManager
from simde import MoleculeFromString


class TestSystemViaMolSSI(unittest.TestCase):
    def test_h2(self):
        corr = make_h2()
        mol_str = "units a.u.\nH 0.0 0.0 0.0\nH 0.0 0.0 1.68185"
        mol = self.mm.run_as(
            self.pt, "ChemicalSystem via QCElemental", mol_str
        )
        compare_molecules(self, corr.molecule, mol)

    def setUp(self):
        if not is_molssi_enabled():
            self.skipTest("MolSSI friend is not enabled!")

        self.mm = ModuleManager()
        load_modules(self.mm)
        self.pt = MoleculeFromString()
