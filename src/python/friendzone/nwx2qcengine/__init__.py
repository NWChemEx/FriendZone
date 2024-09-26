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

from ..friends import is_friend_enabled
import pluginplay as pp
from simde import TotalEnergy, EnergyNuclearGradientStdVectorD
from .call_qcengine import call_qcengine


class QCEngineEnergy(pp.ModuleBase):

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(TotalEnergy())
        self.description("Driver module for calling friends through QCEngine")

        ddesc = 'Implementation detail DO NOT MANUALLY CHANGE!'
        self.add_input('_driver').set_description(ddesc).set_default('energy')
        self.add_input('program').set_description('Friend to call')
        self.add_input('method').set_description('Level of theory')
        self.add_input('basis set').set_description('Name of AO basis set')

    def run_(self, inputs, submods):
        """
        Our strategy here is to use the fact that the inputs to the energy pt
        are a subset of those to the gradient
        """

        egy_pt = TotalEnergy()
        grad_pt = EnergyNuclearGradientStdVectorD()
        _driver = inputs['_driver'].value()

        mol = None
        if _driver == 'energy':
            mol, = egy_pt.unwrap_inputs(inputs)
        elif _driver == 'gradient':
            mol, _ = grad_pt.unwrap_inputs(inputs)
            #TODO verify points is equal to mol
        else:
            raise RuntimeError('Unexpected driver type')

        program = inputs['program'].value()
        method = inputs['method'].value()
        basis = inputs['basis set'].value()
        model = {'method': method, 'basis': basis}
        keywords = {}
        outputs = call_qcengine(_driver,
                                mol,
                                program,
                                self.get_runtime(),
                                model=model,
                                keywords=keywords)

        rv = self.results()
        if _driver == 'gradient':
            grad = outputs['gradient'].flatten().tolist()
            rv = grad_pt.wrap_results(rv, grad)

        return egy_pt.wrap_results(rv, outputs['energy'])


class QCEngineGradient(QCEngineEnergy):

    def __init__(self):
        QCEngineEnergy.__init__(self)
        self.satisfies_property_type(EnergyNuclearGradientStdVectorD())
        self.add_input('_driver').change('gradient')


def load_qcengine_modules(mm):
    """Loads the collection of modules that wrap NWChem calls.

    Currently, the modules in this collection are:

    #.  NWChem : SCF
    #.  NWChem : B3LYP
    #.  NWChem : MP2
    #.  NWChem : CCSD
    #.  NWChem : CCSD(T)
    
    (and their gradients)

    :param mm: The ModuleManager that the NWChem Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """

    for program in ['nwchem']:
        if is_friend_enabled(program):
            for method in ['SCF', 'B3LYP', 'MP2', 'CCSD', 'CCSD(T)']:
                egy_key = program + ' : ' + method
                grad_key = egy_key + ' Gradient'
                mm.add_module(egy_key, QCEngineEnergy())
                mm.add_module(grad_key, QCEngineGradient())

                for key in [egy_key, grad_key]:
                    mm.change_input(key, 'program', program)
                    mm.change_input(key, 'method', method)
