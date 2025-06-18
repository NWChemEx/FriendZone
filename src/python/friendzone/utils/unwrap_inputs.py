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


def _compare_mol_and_point(mol, points):
    """This function is essentially a work around for the comparisons not being
    exposed to Python.
    """
    if mol.size() != points.size():
        return False

    for i in range(mol.size()):
        atom_i = mol.at(i)
        point_i = points.at(i)

        for j in range(3):
            if round(atom_i.coord(j), 16) != round(point_i.coord(j), 16):
                return False

    return True


def unwrap_inputs(pt, inputs):
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
