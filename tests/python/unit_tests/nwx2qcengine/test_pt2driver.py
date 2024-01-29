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

from friendzone.nwx2qcengine.pt2driver import pt2driver
from simde import Energy
import unittest


class NotAPT:
    pass


class Testpt2driver(unittest.TestCase):

    def test_pts_that_map_to_energy(self):
        for pt in [Energy()]:
            self.assertEqual(pt2driver(pt), 'energy')

    def test_bad_pt(self):
        self.assertRaises(Exception, pt2driver, NotAPT())
