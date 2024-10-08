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

import qcengine as qcng
import qcelemental as qcel
from ..nwx2qcelemental.chemical_system_conversions import chemical_system2qc_mol
from qcengine.config import TaskConfig


def call_qcengine(driver, mol, program, runtime, **kwargs):
    """ Wraps calling a program through the QCEngine API.

        .. note::

           QCEngine only supports high-level modularity (modularity roughly at
           the granularity of a call to an electronic structure package). We
           thus have assumed that the molecular system will always be an input
           to whatever QCEngine call we are running.

        This function is the main API for calling QCEngine from NWChemEx. The
        idea is to more or less feed the inputs from a ``run_as`` call directly
        into this function and then have this function convert the NWChemEx
        objects to their QCElemental equivalents. Right now those mappings
        include:

        - ChemicalSystem -> qcel.models.Molecule
        - RuntimeView -> qcng.TaskConfig

        While not supported at the moment, similar conversions for the AO basis
        set are possible.

        Because of the difference in philosophy between QCEngine and NWChemEx,
        there are some inputs which can not easily be mapped automatically, for
        example the electronic structure method (in NWChemEx methods correspond
        to module instances, whereas QCEngine requires strings). It is the
        responsibility of the module wrapping the call to ``call_qcengine`` to
        pass these additional inputs in as kwargs that can be forwarded to a
        QCElemental.models.AtomicInput object via the ``model`` keyword.

        :param pt: The property type we are computing.
        :type pt: pluginplay.PropertyType
        :param mol: The molecular system we are computing the properties of.
        :type mol: chemist.ChemicalSystem
        :param program: Which electronic structure package is being used as the
                        backend?
        :type program: str
        :param kwargs: Key-value pairs which will be forwarded to QCElemental's
                       ``AtomicInput`` class as kwargs.

        :return: A dictionary containing the requested property and any other
                 property of potential interest.
        :rtype: Varies depending on the requested property
    """

    # Step 1: Prepare the chemistry-related input
    qc_mol = chemical_system2qc_mol(mol)
    inp = qcel.models.AtomicInput(molecule=qc_mol, driver=driver, **kwargs)

    # Step 2: Prepare the runtime-related input
    # I *think* ncores is supposed to be the number of threads per MPI rank
    task_config = {'nnodes': runtime.size(), 'ncores': 1, 'retries': 0}

    # Step 3: Run QCEngine
    results = qcng.compute(inp, program, task_config=task_config)

    # Step 4: Verify the computation ran correctly
    if type(results) == qcel.models.common_models.FailedOperation:
        raise RuntimeError(results.error.error_message)

    # Step 5: Prepare the results
    rv = {driver: results.return_result}
    if (driver == "gradient" and "qcvars" in results.extras):
        rv['energy'] = float(results.extras["qcvars"]["CURRENT ENERGY"])
    return rv
