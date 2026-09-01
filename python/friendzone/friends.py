# Copyright 2025 NWChemEx-Project
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

from importlib.util import find_spec
from shutil import which


def is_ase_enabled():
    """Checks whether the ASE friend is enabled.

    :return: True if the ASE friend is enabled, False otherwise.
    :rtype: bool
    """
    return find_spec("ase") is not None


def is_molssi_enabled():
    """Checks whether the MolSSI friend is enabled.

    :return: True if the MolSSI friend is enabled, False otherwise.
    :rtype: bool
    """
    for req in ["qcelemental", "qcengine", "networkx"]:
        if find_spec(req) is None:
            return False
    return True


def is_nwchem_enabled():
    """Checks whether the NWChem friend is enabled.

    :return: True if the NWChem friend is enabled, False otherwise.
    :rtype: bool
    """
    return which("nwchem") is not None
