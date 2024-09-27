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


def _run_impl(driver, inputs, rv, runtime):
    """
    Our strategy here is to use the fact that the inputs to the TotalEnergy 
    PT are a subset of those to other PTs
    """
    # Step 0: Figure out the PT we're being run as
    egy_pt = TotalEnergy()
    grad_pt = EnergyNuclearGradientStdVectorD()

    # Step 1: Unwrap the inputs
    mol = None
    if driver == 'energy':
        mol, = egy_pt.unwrap_inputs(inputs)
    elif driver == 'gradient':
        mol, _ = grad_pt.unwrap_inputs(inputs)
        #TODO: verify ignored second input (the point at which to take the
        #derivative) is equal to the geometry of mol.
    else:
        raise RuntimeError('Unexpected driver type')

    program = inputs['program'].value()
    method = inputs['method'].value()
    basis = inputs['basis set'].value()

    # Step 2: Call QCEngine
    model = {'method': method, 'basis': basis}
    keywords = {}
    outputs = call_qcengine(driver,
                            mol,
                            program,
                            runtime,
                            model=model,
                            keywords=keywords)

    # Step 3: Prepare results
    if driver == 'gradient':
        grad = outputs['gradient'].flatten().tolist()
        rv = grad_pt.wrap_results(rv, grad)

    return egy_pt.wrap_results(rv, outputs['energy'])


class QCEngineEnergy(pp.ModuleBase):
    """ Driver module for computing energies with QCEngine"""

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.satisfies_property_type(TotalEnergy())
        self.description(QCEngineEnergy.__doc__)
        self.add_input('program').set_description('Friend to call')
        self.add_input('method').set_description('Level of theory')
        self.add_input('basis set').set_description('Name of AO basis set')

    def run_(self, inputs, submods):
        return _run_impl('energy', inputs, self.results(), self.get_runtime())


class QCEngineGradient(QCEngineEnergy):
    """ This class is largely implemented by QCEngineEnergy. The only difference
        is in the ctor. The differences are:

        - Property type is set to EnergyNuclearGradientStdVectorD
        - An internal implementation detail is modified to signal the modified
          property type.
    """

    def __init__(self):
        QCEngineEnergy.__init__(self)
        self.satisfies_property_type(EnergyNuclearGradientStdVectorD())

    def run_(self, inputs, submods):
        return _run_impl('gradient', inputs, self.results(),
                         self.get_runtime())


def load_qcengine_modules(mm):
    """Loads the collection of modules that wrap QCElemental calls.

    Currently, the friends exported by this function are:
    
    #. NWChem

    the levels of theory are: 

    #. SCF
    #. B3LYP
    #. MP2
    #. CCSD
    #. CCSD(T)

    and we have 0-th and 1-st derivatives.
    
    The final set of modules is the Cartesian product of all of the above.

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
