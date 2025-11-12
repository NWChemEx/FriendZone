# Copyright 2025 NWChemEx-Project
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
from importlib.util import find_spec
from shutil import which

from friendzone import friends


class TestFriends(unittest.TestCase):
    def test_is_ase_enabled(self):
        expected = find_spec("ase") is not None
        actual = friends.is_ase_enabled()
        self.assertEqual(expected, actual)

    def test_is_molssi_enabled(self):
        expected = True
        for req in ["qcelemental", "qcengine", "networkx"]:
            if find_spec(req) is None:
                expected = False
                break
        actual = friends.is_molssi_enabled()
        self.assertEqual(expected, actual)

    def test_is_nwchem_enabled(self):
        expected = which("nwchem") is not None
        actual = friends.is_nwchem_enabled()
        self.assertEqual(expected, actual)
