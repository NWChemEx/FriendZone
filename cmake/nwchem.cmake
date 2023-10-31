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

include_guard()
include(python/python)

#[[[ Determines if NWChem and the necessary Python interface are installed.
#
#  At present FriendZone can not install
#]]
function(find_nwchem)
    find_program(NWCHEM_FOUND nwchem REQUIRED)
    assert_python_module("qcelemental")
    assert_python_module("qcengine")
    assert_python_module("networkx")
    message("Found nwchem: ${NWCHEM_FOUND}")
endfunction()

if("${ENABLE_NWCHEM}")
    find_nwchem()
endif()
