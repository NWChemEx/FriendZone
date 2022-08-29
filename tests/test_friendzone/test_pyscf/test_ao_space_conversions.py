import unittest
from pyscf import gto
from friendzone.pyscf.ao_space_conversions import atom_to_ao, convert_to_pyscf
from mokup import mokup
from .test_pyscf import string_geoms, compare_pyscf_basis, compare_pyscf_mol
import pyscf


class TestAOSpaceConversions(unittest.TestCase):
    ''' Tests functionality found in the friendzone.pyscf.ao_space_conversions
    module.

    :param nwx_aos: A dictionary mapping molecule names to their AO basis sets.
    :type nwx_aos: dict(str, chemist.orbital_space.AOSpaceD)

    :param pyscf_mols: A dictionary mapping molecule names to PySCF Mole
        objects. The state of the Mole objects is consistent with calling
        ``molecule_conversions.convert_to_pyscf``.
    :type pyscf_mols: dict(str, pyscf.gto.Mole)

    :param pyscf_mols_and_aos: Similar to ``pyscf_mos``, but also contains the
        AO basis set. These are the correct answers.
    :type pyscf_mols_and_aos: dict(str, pyscf.gto.Mole)
    '''

    def setUp(self):
        '''Initializes the attributes'''
        geoms = string_geoms()

        bs = mokup.basis_set.sto3g
        self.nwx_aos = {
            'H2': mokup.get_bases(mokup.molecule.h2, bs),
            'H2_2': mokup.get_bases(mokup.molecule.h2_2, bs),
            'H2O': mokup.get_bases(mokup.molecule.h2o, bs)
        }
        self.pyscf_mols = {
            'H2': gto.M(atom=geoms['H2'], unit='B'),
            'H2_2': gto.M(atom=geoms['H2_2'], unit='B'),
            'H2O': gto.M(atom=geoms['H2O'], unit='B')
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
            'H2': gto.M(atom=geoms['H2'], unit='B', basis=h2_basis),
            'H2_2': gto.M(atom=geoms['H2_2'], unit='B', basis=h2_2_basis),
            'H2O': gto.M(atom=geoms['H2O'], unit='B', basis=h2o_basis),
            'H2(H2)': gto.M(atom=geoms['H2(H2)'], unit='B', basis=h2_h2_basis)
        }

    def test_atom_to_ao(self):
        '''Tests atom_to_ao

        At the moment ``atom_to_ao`` is somewhat simplistic so the main testing
        point is that the resulting list is correct.
        '''

        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            atom2center = atom_to_ao(pyscf_mol, aos)
            corr = [i for i in range(pyscf_mol.natm)]
            self.assertEqual(atom2center, corr)

    def test_convert_to_pyscf(self):
        '''Tests convert_to_pyscf when there are no ghost atoms present.

        This unit test assumes that atom_to_ao always works. This unit test
        also assumes that there are no ghost atoms in the system. Subject to
        these assumptions, we check that:
        - the AO basis set parameters are added to the result correctly
        - the atoms are unchanged
        '''
        for mol_name, aos in self.nwx_aos.items():
            pyscf_mol = self.pyscf_mols[mol_name]
            pyscf_mol = convert_to_pyscf(aos, pyscf_mol)
            corr = self.pyscf_mols_and_aos[mol_name]
            compare_pyscf_basis(self, pyscf_mol, corr)
            compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_to_pyscf_ghost_atoms(self):
        '''Tests convert_to_pyscf when there are ghost atoms present.

        This unit test is similar to ``test_convert_to_pyscf``, but we
        now know we have ghost atoms in the system. Here we check that:
        - the AO basis set parameters are added to the result correctly
        - the atoms are updated with ghost atoms
        '''
        pyscf_mol = self.pyscf_mols['H2']
        aos = self.nwx_aos['H2_2']
        pyscf_mol = convert_to_pyscf(aos, pyscf_mol)

        corr = self.pyscf_mols_and_aos['H2(H2)']
        compare_pyscf_basis(self, pyscf_mol, corr)
        compare_pyscf_mol(self, pyscf_mol, corr)

    def test_convert_to_pyscf_error_checking(self):
        ''' Tests the error checking capabilities of convert_to_pyscf

        At the moment the error checking in ``convert_to_pyscf`` amounts to
        detecting inconcistencies in the number of centers/atoms.
        '''

        pyscf_h2 = self.pyscf_mols['H2']
        pyscf_h2_2 = self.pyscf_mols['H2_2']
        nwx_h2 = self.nwx_aos['H2']

        # Declare short variables to help assertions fit on one line
        fxn = convert_to_pyscf
        a_exp = AssertionError

        # This passes an AOSpace with two centers when there are four real
        # atoms, in turn len(nwx_ao_space) < pyscf_mol.natm is tripped.
        self.assertRaises(a_exp, fxn, nwx_h2, pyscf_h2_2)


if __name__ == '__main__':
    unittest.main()
