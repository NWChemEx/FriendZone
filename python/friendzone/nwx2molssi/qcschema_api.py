# Copyright 2026 NWChemEx-Project
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

import pluginplay as pp


class QCSchemaAPI(pp.PythonOnlyPropertyType):
    """The API for computing a MolSSI QCSchema AtomicResult from an
    AtomicInput.

    Both the input and the result are opaque Python objects (in practice
    ``qcelemental.models.AtomicInput``/``AtomicResult`` instances), which is
    why this property type is defined purely in Python via
    ``pluginplay.PythonOnlyPropertyType`` rather than as a typed C++
    property type.
    """

    def __init__(self):
        pp.PythonOnlyPropertyType.__init__(self, "QCSchemaAPI")
        self.declare_input("Atomic Input").set_description(
            "A qcelemental.models.AtomicInput instance describing the "
            "computation to run"
        )
        self.declare_result("Atomic Result").set_description(
            "A qcelemental.models.AtomicResult instance holding the "
            "results of the computation"
        )
