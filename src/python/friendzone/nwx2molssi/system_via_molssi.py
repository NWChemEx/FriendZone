# Copyright 2025 NWChemEx
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

import pluginplay as pp
import qcelemental
from simde import MoleculeFromString

from .chemical_system_conversions import qc_mol2molecule


class SystemViaMolSSI(pp.ModuleBase):
    """Creates an NWChemEx ChemicalSystem by going through MolSSI's string
    parser.
    """

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(MoleculeFromString())
        self.description(SystemViaMolSSI.__doc__)

    def run_(self, inputs, submods):
        pt = MoleculeFromString()
        (mol_str,) = pt.unwrap_inputs(inputs)
        mol = qc_mol2molecule(qcelemental.models.Molecule.from_data(mol_str))

        rv = self.results()
        return pt.wrap_results(rv, mol)


def load_system_via_molssi_modules(mm):
    """Loads the collection of modules that wrap QCElemental calls.

    :param mm: The ModuleManager that the NWChem Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    mm.add_module("ChemicalSystem via QCElemental", SystemViaMolSSI())
