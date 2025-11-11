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

from friendzone.friends import friends, is_friend_enabled


class TestFriends(unittest.TestCase):
    def test_friends_list(self):
        expected_friends = ["ase", "nwchem"]
        actual_friends = friends()
        self.assertCountEqual(actual_friends, expected_friends)

    def test_is_friend_enabled(self):
        # For known friends, the result should match the system state
        for friend in friends():
            enabled = is_friend_enabled(friend)
            module_found = find_spec(friend) is not None
            self.assertEqual(enabled, module_found)
        # For unknown friends, the result should be False
        self.assertFalse(is_friend_enabled("non_existent_friend"))
