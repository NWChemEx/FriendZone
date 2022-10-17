import unittest
import friendzone.nwx_pyscf
from simde import simde, chemist, pluginplay
from mokup import mokup


class TestRMP2Energy(unittest.TestCase):
    '''Tests functionality found in the friendzone.nwx_pyscf.rmp2_energy module.

    :param molecules: A list of molecules to run
    :type molecules: list(mokup.molecule)

    :param bs: A list of basis sets to run
    :type bs: list(mokup.basis_set)

    :param corr: Map from molecule-basis set pairs to its total MP2 energy.
    :type corr: dict(tuple(mokup.molecule, mokup.basis_set), float)
    '''

    def setUp(self):
        '''Initializes the attributes.'''
        h2 = mokup.molecule.h2
        h2_2 = mokup.molecule.h2_2
        h2o = mokup.molecule.h2o
        sto3g = mokup.basis_set.sto3g

        self.molecules = [h2, h2_2, h2o]
        self.bs = [sto3g]
        self.corr = {
            (h2, sto3g): -1.1112481262263467,
            (h2_2, sto3g): -2.2224962465716924,
            (h2o, sto3g): -74.99122976221274
        }

    def test_rmp2_energy(self):
        '''Tests the run member of the RMP2Energy class.

        This unit test loops over all molecule-basis set pairs, computes the
        MP2 energy of the input, and then compares the energy to the reference
        values.
        '''

        mm = pluginplay.ModuleManager()
        friendzone.nwx_pyscf.load_modules(mm)

        for m_mol in self.molecules:
            for m_aos in self.bs:
                mol = mokup.get_molecule(m_mol)
                sys = chemist.ChemicalSystem(mol)
                aos = mokup.get_bases(m_mol, m_aos)

                [e] = mm.at("PySCF RMP2").run_as[simde.AOEnergy](aos, sys)
                self.assertAlmostEqual(e, self.corr[(m_mol, m_aos)], places=5)
