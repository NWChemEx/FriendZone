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

import uuid

import numpy as np
import pluginplay as pp
import tensorwrapper as tw
from ase import units
from ase.calculators.nwchem import NWChem
from simde import EnergyNuclearGradientStdVectorD, TotalEnergy

from ..friends import is_nwchem_enabled
from ..utils.unwrap_inputs import unwrap_inputs
from .chemical_system_conversions import chemical_system2atoms


class NWChemEnergyViaASE(pp.ModuleBase):
    """Driver module for computing energies with NWChem through ASE."""

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.description(NWChemEnergyViaASE.__doc__)
        self.satisfies_property_type(TotalEnergy())
        self.add_input("method").set_description("The level of theory to use.")
        self.add_input("basis set").set_description(
            "The atomic basis set to use."
        )

    def run_(self, inputs, submods):
        pt = TotalEnergy()
        method = inputs["method"].value()
        basis = inputs["basis set"].value()
        mol = unwrap_inputs(pt, inputs)
        atoms = chemical_system2atoms(mol)

        atoms.calc = NWChem(
            theory=method, basis=basis, task="Energy", label=str(uuid.uuid4())
        )
        egy = atoms.get_potential_energy()
        egy = tw.Tensor(np.array(egy / units.Hartree))

        rv = self.results()
        return pt.wrap_results(rv, egy)


class NWChemGradientViaASE(pp.ModuleBase):
    """Driver module for computing energy gradients with ASE."""

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.description(NWChemGradientViaASE.__doc__)
        self.satisfies_property_type(TotalEnergy())
        self.satisfies_property_type(EnergyNuclearGradientStdVectorD())
        self.add_input("method").set_description("The level of theory to use.")
        self.add_input("basis set").set_description(
            "The atomic basis set to use."
        )

    def run_(self, inputs, submods):
        pt = EnergyNuclearGradientStdVectorD()
        method = inputs["method"].value()
        basis = inputs["basis set"].value()
        mol = unwrap_inputs(pt, inputs)
        atoms = chemical_system2atoms(mol)

        atoms.calc = NWChem(
            theory=method,
            basis=basis,
            task="Gradient",
            label=str(uuid.uuid4()),
        )
        egy = atoms.get_potential_energy()  # units are eV
        grad = atoms.get_forces().flatten().tolist()  # units are ev / Ang

        rv = self.results()
        au2eV = units.Hartree  # Hartree to eV conversion
        au2ang = units.Bohr  # Bohr to Angstrom conversion
        # We get the FORCE back NOT the gradient (i.e., need to multiply by -1)
        egy = tw.Tensor(np.array(egy / au2eV))
        augrad = [-1.0 * x / (au2eV / au2ang) for x in grad]
        rv = TotalEnergy().wrap_results(rv, egy)
        return pt.wrap_results(rv, augrad)


def load_nwchem_via_ase_modules(mm):
    """Loads the collection of all ASE(NWChem) modules.

    .. note::

        This function is a no-op if NWChem is not installed.

    :param mm: The ModuleManager that the all Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    if is_nwchem_enabled():
        # Loop over methods and add energy and gradient modules for each
        for method in ["SCF", "MP2", "CCSD", "CCSD(T)"]:
            egy_key = "ASE(NWChem) : " + method
            grad_key = egy_key + " gradient"

            mm.add_module(egy_key, NWChemEnergyViaASE())
            mm.add_module(grad_key, NWChemGradientViaASE())

            for key in [egy_key, grad_key]:
                mm.change_input(key, "method", method)
