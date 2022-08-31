from simde import simde, chemist, pluginplay
from . import chemical_system_conversions
from . import ao_space_conversions
import pyscf


class RHFEnergy(pluginplay.ModuleBase):
    '''Computes the restricted SCF energy of a molecule/AO basis set pair by
    calling PySCF.
    '''

    def __init__(self):
        '''Standard module ctor'''

        super().__init__(self)
        self.description(RHFEnergy.__doc__)
        self.satisfies_property_type[simde.AOEnergy]()

    def run_(self, inputs, submods):
        '''Computes the restricted SCF energy with PySCF'''

        [aos, sys] = simde.AOEnergy.unwrap_inputs(inputs)

        # Add state from ChemcialSystem
        mol = chemical_system_conversions.convert_to_pyscf(sys)

        # Add state from AOSpace class
        mol = ao_space_conversions.convert_to_pyscf(aos, mol)

        mol.verbose = 0

        # Run the energy
        rhf = pyscf.scf.RHF(mol)
        egy = rhf.kernel()  # N.B. egy comes back as a numpy.float64

        rv = self.results()
        return simde.AOEnergy.wrap_results(rv, float(egy))
