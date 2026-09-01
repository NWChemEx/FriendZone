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

from friendzone import load_modules
from friendzone.friends import is_molssi_enabled

if is_molssi_enabled():
    import numpy as np
    import qcelemental as qcel
    import tensorwrapper
    from pluginplay import ModuleBase, ModuleManager
    from simde import AOEnergy

    from friendzone.nwx2molssi.qcschema_api import QCSchemaAPI

    class DummyAOEnergyModule(ModuleBase):
        def __init__(self):
            ModuleBase.__init__(self)
            self.satisfies_property_type(AOEnergy())

        def run_(self, inputs, submods):
            rv = self.results()
            e = tensorwrapper.Tensor(np.array(-3.14))
            return AOEnergy().wrap_results(rv, e)


def make_water_input(basis, driver="energy"):
    water_str = (
        "units a.u.\n"
        "O 0.0 0.0 0.219814\n"
        "H 0.0 1.419470 -0.879257\n"
        "H 0.0 -1.419470 -0.879257"
    )
    mol = qcel.models.v2.Molecule.from_data(water_str)
    model = qcel.models.v2.Model(method="hf", basis=basis)
    spec = qcel.models.v2.AtomicSpecification(driver=driver, model=model)
    return qcel.models.v2.AtomicInput(molecule=mol, specification=spec)


def make_sto_3g_like_basis():
    o_shell = qcel.models.v2.ElectronShell(
        angular_momentum=[0],
        harmonic_type="cartesian",
        exponents=[130.70932, 23.808861, 6.4436083],
        coefficients=[[0.15432897, 0.53532814, 0.44463454]],
    )
    h_shell = qcel.models.v2.ElectronShell(
        angular_momentum=[0],
        harmonic_type="cartesian",
        exponents=[3.42525091, 0.62391373, 0.16885540],
        coefficients=[[0.15432897, 0.53532814, 0.44463454]],
    )
    o_center = qcel.models.v2.BasisCenter(electron_shells=[o_shell])
    h_center = qcel.models.v2.BasisCenter(electron_shells=[h_shell])
    return qcel.models.v2.BasisSet(
        name="sto-3g-like",
        center_data={"o": o_center, "h": h_center},
        atom_map=["o", "h", "h"],
    )


class TestQCSchemaDriver(unittest.TestCase):
    def test_energy(self):
        atomic_input = make_water_input(self.basis)
        result = self.mm.run_as(self.pt, "QCSchema Driver", atomic_input)

        self.assertTrue(result.success)
        self.assertAlmostEqual(result.return_result, -3.14, places=6)
        self.assertAlmostEqual(result.properties.return_energy, -3.14, places=6)

    def test_unsupported_driver_fails_gracefully(self):
        atomic_input = make_water_input(self.basis, driver="gradient")
        result = self.mm.run_as(self.pt, "QCSchema Driver", atomic_input)

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_named_basis_fails_gracefully(self):
        atomic_input = make_water_input("sto-3g")
        result = self.mm.run_as(self.pt, "QCSchema Driver", atomic_input)

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def setUp(self):
        if not is_molssi_enabled():
            self.skipTest("MolSSI friend is not enabled!")

        self.mm = ModuleManager()
        load_modules(self.mm)
        self.mm.add_module("Dummy AOEnergy", DummyAOEnergyModule())
        self.mm.change_submod(
            "QCSchema Driver", "AOEnergy", "Dummy AOEnergy"
        )

        self.pt = QCSchemaAPI()
        self.basis = make_sto_3g_like_basis()
