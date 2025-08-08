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

from .nwx2ase import load_ase_modules
from .nwx2qcelemental import load_qcelemental_modules
from .nwx2qcengine import load_qcengine_modules


def load_modules(mm):
    """Loads the collection of all modules provided by Friendzone. This function
    calls the various friend specific module loading functions, including:

    *  `load_ase_modules`
    *  `load_qcengine_modules`
    *  `load_qcelemental_modules`

    Note some and/or all of these may be no-ops depending on what friends were
    enabled.

    :param mm: The ModuleManager that the all Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    load_ase_modules(mm)
    load_qcengine_modules(mm)
    load_qcelemental_modules(mm)
