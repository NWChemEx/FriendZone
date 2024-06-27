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
from simde import TotalEnergy
from simde import EnergyNuclearGradientStdVectorD
from ..nwx2qcengine.call_qcengine import call_qcengine


class NWChemViaMolSSI(pp.ModuleBase):

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(TotalEnergy())
        self.description("Calls NWChem via MolSSI's QCEngine")
        self.add_input('method')
        self.add_input("basis set")
        self.add_input("keywords").set_default({})
        self.add_input("MPI config").set_default(None)  # Kazuumi addition

    def run_(self, inputs, submods):
        pt = TotalEnergy()
        mol, = pt.unwrap_inputs(inputs)
        method = inputs['method'].value()
        basis = inputs['basis set'].value()
        keywords = inputs['keywords'].value()
        MPIconfig = inputs['MPI config'].value()  # Kazuumi addition

        model = {"method": method, "basis": basis}
        e = call_qcengine(pt,
                          mol,
                          'nwchem',
                          MPIconfig,
                          model=model,
                          keywords=keywords)  # Kazuumi addition
        rv = self.results()
        return pt.wrap_results(rv, e)


class NWChemGradientViaMolSSI(pp.ModuleBase):

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(EnergyNuclearGradientStdVectorD())
        self.description("Calls NWChem via MolSSI's QCEngine")
        self.add_input('method')
        self.add_input("basis set")
        self.add_input("keywords").set_default({})
        self.add_input("MPI config").set_default(None)  # Kazuumi addition

    def run_(self, inputs, submods):
        pt = EnergyNuclearGradientStdVectorD()
        #       mol, = pt.unwrap_inputs(inputs)             # old version
        mol, pointset1 = pt.unwrap_inputs(inputs)  # new version
        method = inputs['method'].value()
        basis = inputs['basis set'].value()
        keywords = inputs['keywords'].value()
        MPIconfig = inputs['MPI config'].value()  # Kazuumi addition

        model = {"method": method, "basis": basis}
        e, f = call_qcengine(pt,
                             mol,
                             'nwchem',
                             MPIconfig,
                             model=model,
                             keywords=keywords)  # Kazuumi addition
        f = [c for cs in f for c in cs]  # Flatten out the list of lists
        rv = self.results()
        return pt.wrap_results(rv, f)


class NWChemEnergyAndGradientViaMolSSI(pp.ModuleBase):

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(EnergyNuclearGradientStdVectorD())
        self.description("Calls NWChem via MolSSI's QCEngine")
        self.add_input('method')
        self.add_input("basis set")
        self.add_input("keywords").set_default({})
        self.add_input("MPI config").set_default(None)  # Kazuumi addition

    def run_(self, inputs, submods):
        pt = EnergyNuclearGradientStdVectorD()
        #       mol, = pt.unwrap_inputs(inputs)             # old version
        mol, pointset1 = pt.unwrap_inputs(inputs)  # new version
        method = inputs['method'].value()
        basis = inputs['basis set'].value()
        keywords = inputs['keywords'].value()
        MPIconfig = inputs['MPI config'].value()  # Kazuumi addition

        model = {"method": method, "basis": basis}
        e, f = call_qcengine(pt,
                             mol,
                             'nwchem',
                             MPIconfig,
                             model=model,
                             keywords=keywords)  # Kazuumi addition
        combined_ef = [c for cs in f
                       for c in cs]  # Flatten out the list of lists
        combined_ef.append(e)
        rv = self.results()
        return pt.wrap_results(rv, combined_ef)


def load_nwchem_modules(mm):
    """Loads the collection of modules that wrap NWChem calls.

    Currently, the modules in this collection are:

    #.  NWChem : SCF
    #.  NWChem : MP2
    #.  NWChem : B3LYP
    #.  NWChem : CCSD
    #.  NWChem : CCSD(T)
    #.  NWChem : SCF Gradient
    #.  NWChem : MP2 Gradient
    #.  NWChem : B3LYP Gradient

    :param mm: The ModuleManager that the NWChem Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    if is_friend_enabled('nwchem'):
        for method in ['SCF', 'MP2', 'B3LYP', 'CCSD', 'CCSD(T)']:
            mod_key = 'NWChem : ' + method
            mm.add_module(mod_key, NWChemViaMolSSI())
            mm.change_input(mod_key, 'method', method)

        for method in ['SCF', 'MP2', 'B3LYP']:
            mod_key = 'NWChem : ' + method + ' Gradient'
            mm.add_module(mod_key, NWChemGradientViaMolSSI())
            mm.change_input(mod_key, 'method', method)

        for method in ['SCF', 'MP2', 'B3LYP']:
            mod_key = 'NWChem : ' + method + ' EnergyAndGradient'
            mm.add_module(mod_key, NWChemEnergyAndGradientViaMolSSI())
            mm.change_input(mod_key, 'method', method)
