import unittest
from pyscf import gto
from friendzone.pyscf.ao_space_conversions import convert_to_pyscf
from mokup import mokup


class TestAOSpaceConversions(unittest.TestCase):

    def setUp(self):
        h2 = 'H 0.0 0.0 0.0; H 0.0 0.0 1.6818473865225443'
        h2_2 = '''
            H 0.0 0.0  0.0
            H 0.0 0.0  1.6818473865225443
            H 0.0 0.0 41.6818473865225443
            H 0.0 0.0 43.363694773
            '''
        h2o = '''
            O  0.0               -0.143222342980786 0.0
            H  1.638033502034240  1.136556880358410 0.0
            H -1.638033502034240  1.136556880358410 0.0
            '''
        bs = mokup.basis_set.sto3g
        self.nwx_aos = {
            "H2": mokup.get_bases(mokup.molecule.h2, bs),
            #"H2_2": mokup.get_bases(mokup.molecule.h2_2, bs),
            #"H2O": mokup.get_bases(mokup.molecule.h2o, bs)
        }
        self.pyscf_mols = {
            "H2": gto.M(atom=h2, unit='B'),
            #"H2_2": gto.M(atom=h2_2, unit='B'),
            #"H2O": gto.M(atom=h2o, unit='B')
        }
        self.pyscf_mols_and_aos = {
            "H2": gto.M(atom=h2, unit='B'),
            #"H2_2": gto.M(atom=h2_2, unit='B'),
            #"H2O": gto.M(atom=h2o, unit='B')
        }

    def test_convert_to_pyscf(self):
        """Tests convert_to_pyscf without providing a Mole object"""
        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            atom2center = [i for i in range(pyscf_mol.natm)]
            pyscf_mol = convert_to_pyscf(aos, atom2center, pyscf_mol)
            corr = self.pyscf_mols_and_aos[mol_name]
            #self.compare_pyscf_mol(pyscf_mol, corr)


if __name__ == '__main__':
    unittest.main()
