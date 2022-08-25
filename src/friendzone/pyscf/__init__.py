from . import rhf_energy
from . import rmp2_energy
from simde import simde
from cppyy.gbl.std import make_shared


def load_modules(mm):
    mm.add_module("PySCF RHF", make_shared[rhf_energy.RHFEnergy]())
    mm.add_module("PySCF RMP2", make_shared[rmp2_energy.RMP2Energy]())
