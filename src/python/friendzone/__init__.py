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

from .nwx2nwchem import load_nwchem_modules


def load_modules(mm):
    """Loads the collection of all modules provided by Friendzone. This function
    calls the various friend specific module loading functions, including:

    *  `load_nwchem_modules`
    
    :param mm: The ModuleManager that the all Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    load_nwchem_modules(mm)
