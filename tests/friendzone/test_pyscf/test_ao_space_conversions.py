import unittest
from pyscf import gto
from friendzone.pyscf.ao_space_conversions import atom_to_ao, convert_to_pyscf
from mokup import mokup
from .test_pyscf import compare_pyscf_basis, compare_pyscf_mol
import pyscf


class TestAOSpaceConversions(unittest.TestCase):

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
        h2_h2 = '''
        H0 0.0 0.0  0.0
        H1 0.0 0.0  1.6818473865225443
        ghost_H0 0.0 0.0 41.6818473865225443
        ghost_H1 0.0 0.0 43.363694773
        '''

        bs = mokup.basis_set.sto3g
        self.nwx_aos = {
            'H2': mokup.get_bases(mokup.molecule.h2, bs),
            'H2_2': mokup.get_bases(mokup.molecule.h2_2, bs),
            'H2O': mokup.get_bases(mokup.molecule.h2o, bs)
        }
        self.pyscf_mols = {
            'H2': gto.M(atom=h2, unit='B'),
            'H2_2': gto.M(atom=h2_2, unit='B'),
            'H2O': gto.M(atom=h2o, unit='B')
        }

        h_bs = gto.basis.parse('''
        H S
        3.425250914  0.1543289673
        0.6239137298 0.5353281423
        0.1688554040 0.4446345422
        ''')
        o_bs = gto.basis.parse('''
        O S
        130.7093200 0.15432897
         23.8088610 0.53532814
          6.4436083 0.44463454
        O S
        5.0331513 -0.09996723
        1.1695961  0.39951283
        0.3803890  0.70011547
        O P
        5.0331513 0.15591627
        1.1695961 0.60768372
        0.3803890 0.39195739
        ''')

        h2_basis = {'H0': h_bs, 'H1': h_bs}
        h2_2_basis = {'H0': h_bs, 'H1': h_bs, 'H2': h_bs, 'H3': h_bs}
        h2o_basis = {'O0': o_bs, 'H0': h_bs, 'H1': h_bs}
        h2_h2_basis = {
            'H0': h_bs,
            'H1': h_bs,
            'ghost_H0': h_bs,
            'ghost_H1': h_bs
        }
        self.pyscf_mols_and_aos = {
            'H2': gto.M(atom=h2, unit='B', basis=h2_basis),
            'H2_2': gto.M(atom=h2_2, unit='B', basis=h2_2_basis),
            'H2O': gto.M(atom=h2o, unit='B', basis=h2o_basis),
            'H2(H2)': gto.M(atom=h2_h2, unit='B', basis=h2_h2_basis)
        }

    def test_atom_to_ao(self):
        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            atom2center = atom_to_ao(pyscf_mol, aos)
            corr = [i for i in range(pyscf_mol.natm)]
            self.assertEqual(atom2center, corr)

    def test_convert_to_pyscf(self):
        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            atom2center = [i for i in range(pyscf_mol.natm)]
            pyscf_mol = convert_to_pyscf(aos, atom2center, pyscf_mol)
            corr = self.pyscf_mols_and_aos[mol_name]
            compare_pyscf_basis(self, pyscf_mol, corr)
            compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_to_pyscf_ghost_atoms(self):
        pyscf_mol = self.pyscf_mols['H2']
        aos = self.nwx_aos['H2_2']
        atom2center = [0, 1]
        pyscf_mol = convert_to_pyscf(aos, atom2center, pyscf_mol)

        corr = self.pyscf_mols_and_aos['H2(H2)']
        compare_pyscf_basis(self, pyscf_mol, corr)
        compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_to_pyscf_error_checking(self):
        pyscf_h2 = self.pyscf_mols['H2']
        pyscf_h2_2 = self.pyscf_mols['H2_2']
        nwx_h2 = self.nwx_aos['H2']

        # Declare short variables to help assertions fit on one line
        fxn = convert_to_pyscf
        a_exp = AssertionError

        # This passes an empty list whe the list should contain two elements
        # tripping len(atom2center) != pyscf_mol.natm.
        self.assertRaises(a_exp, fxn, nwx_h2, [], pyscf_h2)

        # This passes an AOSpace with two centers when there are four real
        # atoms, in turn len(nwx_ao_space) < pyscf_mol.natm is tripped.
        atom2center = [0, 1, 2, 3]
        self.assertRaises(a_exp, fxn, nwx_h2, atom2center, pyscf_h2_2)

        # This maps atoms 0 and 1 to center 0 violating the assumption that
        # each atom maps to one (and only one) center
        atom2center = [0, 0]
        self.assertRaises(KeyError, fxn, nwx_h2, atom2center, pyscf_h2)

        # This maps atom 1 and to center 4, but nwx_ao_space only has 2 centers
        atom2center = [0, 4]
        self.assertRaises(KeyError, fxn, nwx_h2, atom2center, pyscf_h2)


if __name__ == '__main__':
    unittest.main()
