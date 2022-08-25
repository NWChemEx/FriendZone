from simde import simde, pluginplay
from . import molecule_conversions
from . import ao_space_conversions
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

        # Add state from Molecule class
        mol = molecule_conversions.convert_to_pyscf(sys.molecule())

        # Add state from AOSpace class
        atom2center = [i for i in range(mol.natm)]
        mol = ao_space_conversions.convert_to_pyscf(aos, atom2center, mol)

        mol.verbose = 0

        # Run the energy
        rhf = pyscf.scf.RHF(mol)
        egy = rhf.kernel()  # N.B. egy comes back as a numpy.float64

        rv = self.results()
        return simde.AOEnergy.wrap_results(rv, float(egy))
