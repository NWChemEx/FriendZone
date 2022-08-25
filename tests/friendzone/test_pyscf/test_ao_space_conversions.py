import unittest
from pyscf import gto
from friendzone.pyscf.ao_space_conversions import convert_to_pyscf
from mokup import mokup


class TestAOSpaceConversions(unittest.TestCase):

    def compare_ao_basis(self, mol, corr):

        # Ensure same number of atoms
        n_atoms = mol.natm
        self.assertEqual(n_atoms, corr.natm)

        for atom in range(n_atoms):
            n_shells = mol.atom_nshells(atom)

            # Ensure same number of shells
            self.assertEqual(n_shells, corr.atom_nshells(atom))

            for shell in range(n_shells):
                # Ensure same angular momentum
                l = mol.bas_angular(shell)
                corr_l = corr.bas_angular(shell)
                self.assertEqual(l, corr_l)

                # Ensure (approximately) equal coefficients
                coefs = mol.bas_ctr_coeff(shell)
                corr_coefs = corr.bas_ctr_coeff(shell)
                for c_i, corr_c_i in zip(coefs, corr_coefs):
                    self.assertAlmostEqual(c_i, corr_c_i)

                # Ensure (approximately) equal exponents
                alpha = mol.bas_exp(shell)
                corr_alpha = corr.bas_exp(shell)
                for a_i, corr_a_i in zip(alpha, corr_alpha):
                    self.assertAlmostEqual(a_i, corr_a_i)

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

        bs = mokup.basis_set.sto3g
        self.nwx_aos = {
            "H2": mokup.get_bases(mokup.molecule.h2, bs),
            "H2_2": mokup.get_bases(mokup.molecule.h2_2, bs),
            "H2O": mokup.get_bases(mokup.molecule.h2o, bs)
        }
        self.pyscf_mols = {
            "H2": gto.M(atom=h2, unit='B'),
            "H2_2": gto.M(atom=h2_2, unit='B'),
            "H2O": gto.M(atom=h2o, unit='B')
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
        self.pyscf_mols_and_aos = {
            "H2": gto.M(atom=h2, unit='B', basis=h2_basis),
            "H2_2": gto.M(atom=h2_2, unit='B', basis=h2_2_basis),
            "H2O": gto.M(atom=h2o, unit='B', basis=h2o_basis)
        }

    def test_convert_to_pyscf(self):
        """Tests convert_to_pyscf without providing a Mole object"""
        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            atom2center = [i for i in range(pyscf_mol.natm)]
            pyscf_mol = convert_to_pyscf(aos, atom2center, pyscf_mol)
            corr = self.pyscf_mols_and_aos[mol_name]
            self.compare_ao_basis(pyscf_mol, corr)


if __name__ == '__main__':
    unittest.main()
