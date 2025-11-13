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
from unittest.mock import patch

from friendzone import friends


@patch("friendzone.friends.find_spec")
@patch("friendzone.friends.which")
class TestFriends(unittest.TestCase):
    def test_is_ase_enabled_when_detected(self, mock_which, mock_find_spec):
        mock_find_spec.return_value = True
        actual = friends.is_ase_enabled()
        self.assertTrue(actual)

    def test_is_ase_enabled_when_not_detected(
        self, mock_which, mock_find_spec
    ):
        mock_find_spec.return_value = None
        actual = friends.is_ase_enabled()
        self.assertFalse(actual)

    def test_is_molssi_enabled_when_detected(self, mock_which, mock_find_spec):
        mock_find_spec.return_value = True
        actual = friends.is_molssi_enabled()
        self.assertTrue(actual)

    def test_is_molssi_enabled_when_not_detected(
        self, mock_which, mock_find_spec
    ):
        mock_find_spec.return_value = None
        actual = friends.is_molssi_enabled()
        self.assertFalse(actual)

    def test_is_nwchem_enabled_when_detected(self, mock_which, mock_find_spec):
        mock_which.return_value = True
        actual = friends.is_nwchem_enabled()
        self.assertTrue(actual)

    def test_is_nwchem_enabled_when_not_detected(
        self, mock_which, mock_find_spec
    ):
        mock_which.return_value = None
        actual = friends.is_nwchem_enabled()
        self.assertFalse(actual)
