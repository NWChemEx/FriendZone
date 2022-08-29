from simde import simde, pluginplay
from . import chemical_system_conversions
from . import ao_space_conversions
import pyscf
import pyscf.mp


class RMP2Energy(pluginplay.ModuleBase):
    '''Computes the restricted MP2 energy of a molecule/AO basis set pair by
    calling PySCF.

    The actual module implementation:
    1. Converts the SimDE inputs in to a PySCF.gto.Mole instance
    2. Computes the RHF wavefunction for the input
    3. Computes the MP2 energy using the wavefunction from 2.
    '''

    def __init__(self):
        '''Standard module ctor.'''

        super().__init__(self)
        self.description(RMP2Energy.__doc__)
        self.satisfies_property_type[simde.AOEnergy]()

    def run_(self, inputs, submods):
        '''Computes the restricted MP2 energy with PySCF.'''

        [aos, sys] = simde.AOEnergy.unwrap_inputs(inputs)

        # Add state from ChemicalSystem class
        mol = chemical_system_conversions.convert_to_pyscf(sys)

        # Add state from AOSpace class
        mol = ao_space_conversions.convert_to_pyscf(aos, mol)

        mol.verbose = 0

        # Run the energy
        mf = pyscf.scf.RHF(mol).run()
        my_mp = pyscf.mp.MP2(mf).run()

        rv = self.results()
        return simde.AOEnergy.wrap_results(rv, float(my_mp.e_tot))
