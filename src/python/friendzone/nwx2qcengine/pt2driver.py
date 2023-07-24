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
    if pt.type() == simde.Energy().type():
        return 'energy'

    raise Exception('PropertyType is not registered')
