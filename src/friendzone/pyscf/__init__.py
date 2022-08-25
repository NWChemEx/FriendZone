from . import rhf_energy
from simde import simde
from cppyy.gbl.std import make_shared

def load_modules(mm):
    mm.add_module("PySCF RHF", make_shared[rhf_energy.RHFEnergy]())
