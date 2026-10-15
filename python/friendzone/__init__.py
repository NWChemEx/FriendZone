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

import pluginplay

from .nwx2ase import load_ase_modules
from .nwx2molssi import load_molssi_modules


class FriendZone(pluginplay.Plugin):
    """The FriendZone plugin.

    Load it into a ModuleManager with
    ``mm.load_plugin(friendzone.FriendZone())``. The plugin's name is
    "friendzone". Its modules are added by the various friend specific module
    loading functions, including:

    *  ``load_ase_modules``
    *  ``load_molssi_modules``

    .. note::

        Some and/or all of these may be no-ops depending on what friends were
        enabled.
    """

    def __init__(self):
        pluginplay.Plugin.__init__(self)
        self.set_name("friendzone")
        load_ase_modules(self)
        load_molssi_modules(self)
