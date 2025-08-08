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
from .nwchem_via_ase import NWChemEnergyViaASE, NWChemGradientViaASE


def load_ase_modules(mm):
    if not is_friend_enabled("ase"):
        return

    if is_friend_enabled("nwchem"):
        for method in ["SCF", "MP2", "CCSD", "CCSD(T)"]:
            egy_key = "ASE(NWChem) : " + method
            grad_key = egy_key + " gradient"
            mm.add_module(egy_key, NWChemEnergyViaASE())
            mm.add_module(grad_key, NWChemGradientViaASE())
            for key in [egy_key, grad_key]:
                mm.change_input(key, "method", method)
