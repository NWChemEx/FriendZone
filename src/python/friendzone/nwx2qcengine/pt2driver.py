import simde

def pt2driver(pt):
    if pt.type() == simde.Energy().type():
        return 'energy'
    raise Exception('PropertyType is not registered')
