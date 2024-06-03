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

from friendzone.nwx2qceelemental.chemical_system_conversions import *
from molecules import make_h2
import qcelemental as qcel
import unittest


class TestChemicalSystem2QC(unittest.TestCase):

    def test_h2(self):
        mol = make_h2()
        qcel_mol = chemical_system2qc_mol(mol)

        h2_as_str = "H 0.0 0.0 0.0\nH 0.0 0.0 0.8899966917653396"
        corr = qcel.models.Molecule.from_data(h2_as_str)
        self.assertEqual(qcel_mol, corr)


class TestQCMol2Molecule(unittest.TestCase):

    def test_h2(self):
        corr = make_h2()
        h2_as_str = "H 0.0 0.0 0.0\nH 0.0 0.0 0.8899966917653396"
        mol = qcel.models.Molecule.from_data(h2_as_str)
        self.assertEqual(qc_mol2molecule(mol), corr)
