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

from friendzone import FriendZone, friends
from pluginplay import ModuleManager


class TestFriendZonePlugin(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(self.plugin.name(), "friendzone")
        self.assertEqual(self.plugin.preferred_providers(), [])

    def test_modules(self):
        modules = self.plugin.get_modules()
        has_molssi = friends.is_molssi_enabled()
        self.assertEqual(modules.count("QCSchema Driver"), int(has_molssi))
        self.assertEqual(
            modules.count("ChemicalSystem via QCElemental"), int(has_molssi)
        )

    def test_load_plugin(self):
        mm = ModuleManager()
        mm.load_plugin(FriendZone())
        self.assertTrue(mm.has_plugin("friendzone"))
        self.assertEqual(mm.size(), self.plugin.get_modules().size())

    def setUp(self):
        self.plugin = FriendZone()
