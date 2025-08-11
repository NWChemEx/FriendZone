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

from chemist import PointSetD
from friendzone.utils.unwrap_inputs import unwrap_inputs
from molecules import make_h2
from simde import (
    EnergyNuclearGradientStdVectorD,
    MoleculeFromString,
    TotalEnergy,
)


class TestUnwrapInputs(unittest.TestCase):
    def test_energy(self):
        inputs = self.egy_pt.wrap_inputs(self.egy_pt.inputs(), self.h2)
        mol = unwrap_inputs(self.egy_pt, inputs)
        self.assertEqual(self.h2, mol)

    def test_grad(self):
        inputs = self.grad_pt.inputs()
        inputs = self.grad_pt.wrap_inputs(inputs, self.h2, self.points)
        mol = unwrap_inputs(self.grad_pt, inputs)
        self.assertEqual(self.h2, mol)

    def test_gradient_bad_point(self):
        inputs = self.grad_pt.inputs()
        inputs = self.grad_pt.wrap_inputs(inputs, self.h2, PointSetD())
        self.assertRaises(RuntimeError, unwrap_inputs, self.grad_pt, inputs)

    def test_bad_property_type(self):
        bad_pt = MoleculeFromString()
        self.assertRaises(RuntimeError, unwrap_inputs, bad_pt, [])

    def setUp(self):
        self.h2 = make_h2()
        nuclei = self.h2.molecule.nuclei.as_nuclei()
        self.points = nuclei.charges.point_set.as_point_set()
        self.egy_pt = TotalEnergy()
        self.grad_pt = EnergyNuclearGradientStdVectorD()
