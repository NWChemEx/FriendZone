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

from ..friends import is_ase_enabled

if is_ase_enabled():
    from .nwchem_via_ase import load_nwchem_via_ase_modules


def load_ase_modules(mm):
    """Loads the collection of all ASE modules.

    This function calls the various submodule specific loading functions,
    including:

    *  ``load_nwchem_via_ase_modules``

    .. note::

        Some and/or all of these may be no-ops depending on what friends were
        enabled. This function is a no-op if ASE is not installed.

    :param mm: The ModuleManager that the all Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    if is_ase_enabled():
        load_nwchem_via_ase_modules(mm)
