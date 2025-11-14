# Copyright 2024 NWChemEx
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

from ..friends import is_molssi_enabled

if is_molssi_enabled():
    from .nwchem_via_molssi import load_nwchem_via_molssi_modules
    from .system_via_molssi import load_system_via_molssi_modules


def load_molssi_modules(mm):
    """Loads the collection of all MolSSI modules.

    This function calls the various submodule specific loading functions,
    including:

    *  ``load_system_via_molssi_modules``
    *  ``load_nwchem_via_molssi_modules``

    .. note::

        Some and/or all of these may be no-ops depending on what friends were
        enabled. This entire function is a no-op if the following dependencies
        are not installed:

        *  ``qcelemental``
        *  ``qcengine``
        *  ``networkx``

    :param mm: The ModuleManager that the all Modules will be loaded into.
    :type mm: pluginplay.ModuleManager
    """
    if is_molssi_enabled():
        load_system_via_molssi_modules(mm)
        load_nwchem_via_molssi_modules(mm)
