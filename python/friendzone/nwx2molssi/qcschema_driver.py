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

import numpy as np
import pluginplay as pp
import qcelemental as qcel
from chemist import ChemicalSystem
from simde import AOEnergy

from .basis_set_conversions import qc_basis2ao_basis_set
from .chemical_system_conversions import qc_mol2molecule
from .qcschema_api import QCSchemaAPI


def _failed_result(atomic_input, error_type, error_message):
    # QCSchema v2 splits failures out of AtomicResult (whose ``success``
    # field is now pinned to Literal[True]) and into a separate
    # FailedOperation model.
    error = qcel.models.v2.ComputeError(
        error_type=error_type, error_message=error_message
    )
    return qcel.models.v2.FailedOperation(input_data=atomic_input, error=error)


class QCSchemaDriver(pp.ModuleBase):
    """Computes a QCSchema AtomicResult by running an AOEnergy submodule.

    The AtomicInput's molecule and basis set are converted to a Chemist
    ChemicalSystem and AOBasisSet, respectively, and fed to an AOEnergy
    submodule; the resulting energy is then wrapped back up as an
    AtomicResult.

    .. note::

       Only ``driver == "energy"`` computations are supported, and the
       AtomicInput's ``specification.model.basis`` must be an inline
       ``qcelemental.models.v2.BasisSet`` (as opposed to a basis-set name
       string, which would require resolving against a basis-set library).
       Requests that do not meet these requirements fail gracefully, i.e.
       they return a ``qcelemental.models.v2.FailedOperation`` with a
       populated ``error`` field, rather than raising.
    """

    def __init__(self):
        pp.ModuleBase.__init__(self)
        self.description(QCSchemaDriver.__doc__)
        self.satisfies_property_type(QCSchemaAPI())
        self.add_submodule(AOEnergy(), "AOEnergy").set_description(
            "Computes the energy of the chemical system in the given AO "
            "basis set"
        )

    def run_(self, inputs, submods):
        pt = QCSchemaAPI()
        (atomic_input,) = pt.unwrap_inputs(inputs)

        if atomic_input.specification.driver != "energy":
            result = _failed_result(
                atomic_input,
                "input_error",
                f"QCSchemaDriver only supports driver == 'energy', got "
                f"'{atomic_input.specification.driver}'",
            )
            rv = self.results()
            return pt.wrap_results(rv, result)

        basis = atomic_input.specification.model.basis
        if not isinstance(basis, qcel.models.v2.BasisSet):
            result = _failed_result(
                atomic_input,
                "input_error",
                "QCSchemaDriver requires an inline "
                "qcelemental.models.v2.BasisSet for model.basis, not a "
                "basis-set name string",
            )
            rv = self.results()
            return pt.wrap_results(rv, result)

        mol = qc_mol2molecule(atomic_input.molecule)
        chem_sys = ChemicalSystem(mol)
        aos = qc_basis2ao_basis_set(atomic_input.molecule, basis)

        egy = submods["AOEnergy"].run_as(AOEnergy(), aos, chem_sys)
        e = float(np.array(egy))

        properties = qcel.models.v2.AtomicProperties(return_energy=e)
        result = qcel.models.v2.AtomicResult(
            input_data=atomic_input,
            molecule=atomic_input.molecule,
            properties=properties,
            return_result=e,
            success=True,
            provenance=qcel.models.v2.Provenance(creator="FriendZone"),
        )

        rv = self.results()
        return pt.wrap_results(rv, result)


def load_qcschema_driver_modules(mm):
    """Loads the QCSchemaDriver module.

    :param mm: The ModuleManager that the QCSchemaDriver module will be
               loaded into.
    :type mm: pluginplay.ModuleManager
    """
    mm.add_module("QCSchema Driver", QCSchemaDriver())
