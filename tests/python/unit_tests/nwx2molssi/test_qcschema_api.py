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

import unittest

from friendzone.friends import is_molssi_enabled

if is_molssi_enabled():
    from friendzone.nwx2molssi.qcschema_api import QCSchemaAPI


class TestQCSchemaAPI(unittest.TestCase):
    def test_name(self):
        self.assertEqual(self.pt.name(), "QCSchemaAPI")

    def test_declared_fields(self):
        self.assertEqual(list(self.pt.inputs().keys()), ["Atomic Input"])
        self.assertEqual(list(self.pt.results().keys()), ["Atomic Result"])
        self.assertEqual(self.pt.input_order(), ["Atomic Input"])
        self.assertEqual(self.pt.result_order(), ["Atomic Result"])

    def test_wrap_and_unwrap_inputs(self):
        wrapped = self.pt.wrap_inputs(self.pt.inputs(), {"driver": "energy"})
        (unwrapped,) = self.pt.unwrap_inputs(wrapped)
        self.assertEqual(unwrapped, {"driver": "energy"})

    def test_wrap_and_unwrap_results(self):
        wrapped = self.pt.wrap_results(self.pt.results(), {"success": True})
        (unwrapped,) = self.pt.unwrap_results(wrapped)
        self.assertEqual(unwrapped, {"success": True})

    def setUp(self):
        if not is_molssi_enabled():
            self.skipTest("MolSSI friend is not enabled!")
        self.pt = QCSchemaAPI()
