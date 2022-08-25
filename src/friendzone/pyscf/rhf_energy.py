from simde import simde, pluginplay
from .molecule_conversions import convert_to_pyscf
import pyscf

module_desc = """
Description
===========

Computes the restricted SCF energy of a molecule/AO basis set pair by
calling PySCF.
"""

class RHFEnergy(pluginplay.ModuleBase):
    def __init__(self):
        super().__init__(self)
        self.description(module_desc)
        self.satisfies_property_type[simde.AOEnergy]()

    def run_(self, inputs, submods):
        [aos, sys] = simde.AOEnergy.unwrap_inputs(inputs)

        mol = convert_to_pyscf(sys.molecule())
        mol.basis = 'sto-3g'
        mol.build()

        rhf = pyscf.scf.RHF(mol)
        egy = rhf.kernel() # N.B. egy comes back as a numpy.float64


        rv = self.results()
        return simde.AOEnergy.wrap_results(rv, float(egy))
