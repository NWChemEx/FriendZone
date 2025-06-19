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

from simde import TotalEnergy, EnergyNuclearGradientStdVectorD
import numpy as np



def _compare_mol_and_point(mol, points, atol=1e-12, rtol=0.0):
    """
    Compare the 3D nuclear coordinates of a Molecule and a PointSet.

    This function is intended to ensure that gradient calculations
    are being performed at the correct molecular geometry.

    Parameters
    ----------
    mol : chemist.Molecule
        The molecule whose nuclear coordinates are being compared.

    points : chemist.PointSet
        The point set to compare against (usually created from the molecule's nuclei).

    atol : float, optional
        Absolute tolerance used by np.isclose. Default is 1e-12.
        This catches numerical noise due to Python/C++ floating-point boundary.

    rtol : float, optional
        Relative tolerance used by np.isclose. Default is 0.0 (disabled),
        which ensures no scaling with magnitude — appropriate for comparing coordinates.

    Returns
    -------
    bool
        True if all coordinate components match within the given tolerances.
        False otherwise.

    Notes
    -----
    Exact floating-point equality is not used because of small differences
    (e.g., ~1e-314) introduced by Python/C++ interoperability. These are
    not chemically meaningful and should be tolerated with a small `atol`.
    """
    if mol.size() != points.size():
        return False

    for i in range(mol.size()):
        atom_i = mol.at(i)
        point_i = points.at(i)

        for j in range(3):
            a = atom_i.coord(j)
            b = point_i.coord(j)

            if rtol == 0.0 and atol == 0.0:
                # Strict comparison: values must be bitwise identical
                if a != b:
                    return False
            else:
                # Use np.isclose to allow for floating-point tolerance
                if not np.isclose(a, b, atol=atol, rtol=rtol):
                    return False

    return True


def unwrap_inputs(pt, inputs, atol=1e-12, rtol=0.0):
    """ Code factorization for unwrapping a module's inputs.
    
    Many of our friends expose interfaces which are analogous to high-level
    property types like TotalEnergy, AOEnergy, and EnergyNuclearGradient.
    Furthermore, most of our friends expose all of these calculations through
    a single interface. The result is that many of our modules start by having
    dispatch logic akin to "if we're doing an energy calculation, unwrap this
    way." Or "if we're doing a gradient, unwrap this other way." This function
    factors that logic out into a single function.
    """

    mol = None
    if pt.type() == TotalEnergy().type():
        mol, = pt.unwrap_inputs(inputs)
    elif pt.type() == EnergyNuclearGradientStdVectorD().type():
        mol, point = pt.unwrap_inputs(inputs)

        if not _compare_mol_and_point(mol.molecule, point):
            raise RuntimeError(
                'Derivative must be computed at molecular geometry')
    else:
        raise RuntimeError('Property type: ' + str(pt.type()) +
                           ' is not registered')

    return mol
