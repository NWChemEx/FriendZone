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

from ..friends import is_friend_enabled
import pluginplay as pp
from simde import Energy
from ..nwx2qcengine.call_qcengine import call_qcengine


class NWChemViaMolSSI(pp.ModuleBase):

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(Energy())
        self.description("Calls NWChem via MolSSI's QCEngine")
        self.add_input('method')
        self.add_input("basis set")

    def run_(self, inputs, submods):
        pt = Energy()
        mol, = pt.unwrap_inputs(inputs)
        method = inputs['method'].value()
        basis = inputs['basis set'].value()

        e = call_qcengine(pt, mol, 'nwchem', method=method, basis=basis)
        rv = self.results()
        return pt.wrap_results(rv, e)


if is_friend_enabled('nwchem'):

    def load_nwchem_modules(mm):
        for method in ['SCF', 'mp2', 'ccsd', 'ccsd(t)']:
            mod_key = 'NWChem : ' + method
            mm.add_module(mod_key, NWChemViaMolSSI())
            mm.change_input(mod_key, 'method', method)
else:

    def load_nwchem_modules(mm):
        pass
