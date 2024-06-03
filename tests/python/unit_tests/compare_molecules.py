# Copyright 2024 NWChemEx
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


def compare_molecules(self, lhs, rhs):
    self.assertEqual(lhs.charge(), rhs.charge())
    self.assertEqual(lhs.multiplicity(), rhs.multiplicity())
    self.assertEqual(lhs.size(), rhs.size())
    for i in range(lhs.size()):
        lhs_i = lhs.at(i)
        rhs_i = rhs.at(i)
        self.assertEqual(lhs_i.name, rhs_i.name)
        self.assertEqual(lhs_i.Z, rhs_i.Z)
        self.assertAlmostEqual(lhs_i.mass, rhs_i.mass)
        self.assertAlmostEqual(lhs_i.x, rhs_i.x)
        self.assertAlmostEqual(lhs_i.y, rhs_i.y)
        self.assertAlmostEqual(lhs_i.z, rhs_i.z)
