import unittest
from pyscf import gto
from friendzone.pyscf.molecule_conversions import (convert_to_pyscf,
                                                   convert_from_pyscf)
from mokup import mokup
from .test_pyscf import compare_pyscf_mol


class TestMoleculeConversions(unittest.TestCase):

    def setUp(self):
        h2 = 'H0 0.0 0.0 0.0; H1 0.0 0.0 1.6818473865225443'
        h2_2 = '''
            H0 0.0 0.0  0.0
            H1 0.0 0.0  1.6818473865225443
            H2 0.0 0.0 41.6818473865225443
            H3 0.0 0.0 43.363694773
            '''
        h2o = '''
            O0  0.0               -0.143222342980786 0.0
            H0  1.638033502034240  1.136556880358410 0.0
            H1 -1.638033502034240  1.136556880358410 0.0
            '''
        self.nwx_mols = {
            "H2": mokup.get_molecule(mokup.molecule.h2),
            "H2_2": mokup.get_molecule(mokup.molecule.h2_2),
            "H2O": mokup.get_molecule(mokup.molecule.h2o)
        }
        self.pyscf_mols = {
            "H2": gto.M(atom=h2, unit='B'),
            "H2_2": gto.M(atom=h2_2, unit='B'),
            "H2O": gto.M(atom=h2o, unit='B')
        }

    def test_convert_to_pyscf(self):
        """Tests convert_to_pyscf without providing a Mole object"""
        for mol_name, mol in self.nwx_mols.items():
            pyscf_mol = convert_to_pyscf(mol)
            corr = self.pyscf_mols[mol_name]
            compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_to_pyscf_no_default(self):
        """Tests convert_to_pyscf by providing a Mole object"""
        for mol_name, mol in self.nwx_mols.items():
            pyscf_mol = gto.Mole()
            pyscf_mol.spin = 2
            pyscf_mol = convert_to_pyscf(mol, pyscf_mol)
            corr = self.pyscf_mols[mol_name]

            # Make sure spin is unchanged
            self.assertEqual(pyscf_mol.spin, 2)

            # Compare the rest of the state
            compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_from_pyscf(self):
        for mol_name, mol in self.pyscf_mols.items():
            nwx_mol = convert_from_pyscf(mol)
            corr = self.nwx_mols[mol_name]

            # Ensure same number of atoms
            self.assertEqual(nwx_mol.size(), corr.size())

            # Compare atoms
            for atom_i, corr_i in zip(nwx_mol, corr):
                # Compare atomic number
                self.assertEqual(atom_i.Z(), corr_i.Z())

                # Compare coords
                for q in range(3):
                    self.assertAlmostEqual(atom_i[q], corr_i[q])


if __name__ == '__main__':
    unittest.main()
