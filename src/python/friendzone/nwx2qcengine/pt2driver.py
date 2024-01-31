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

import simde


def pt2driver(pt):
    """ Converts a SimDE property type to a QCElemental driver type.

    Within NWChemEx users pick the property to compute by specifying a
    property type. Within QCElemental this is done by specifying a string.
    This function maps SimDE property types to their corresponding QCElemental
    string.

    :param pt: The property type we are converting.
    :type pt: pluginplay.PropertyType

    :raises: Exception if ``pt`` is not a property type which has been
             registered with this function.
    """
    if pt.type() == simde.TotalEnergy().type():
        return 'energy'

    raise Exception('PropertyType is not registered')
