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


class ASEEnergy(pp.ModuleBase):
    """Driver module for computing energies with ASE."""

    def __init__(self):
        pp.ModuleBase._init__(self)
        self.description(ASEEnergy.__doc__)

    def run_(self, inputs, submods):
        pass
