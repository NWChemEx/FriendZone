import unittest
from simde import chemist
from pyscf import gto
from friendzone.nwx_pyscf.chemical_system_conversions import convert_to_pyscf
from mokup import mokup
from .test_nwx_pyscf import string_geoms, compare_pyscf_mol


class TestChemicalSystemConversions(unittest.TestCase):
    ''' Tests functionality found in the
    friendzone.nwx_pyscf.chemical_system_conversions module.

    :param nwx_mols: A dictionary mapping molecule names to the corresponding
        Molecule object.
    :type nwx_mols: dict(str, chemist.Molecule)

    :param pyscf_mols: A dictionary mapping molecule names to PySCF Mole
        objects. The values are the expected result of calling
        ``molecule_conversion.convert_to_pyscf`` and are used to construct
        the reference values.
    :type pyscf_mols: dict(str, pyscf.gto.Mole)
    '''

    def setUp(self):
        '''Initializes the attributes'''

        geoms = string_geoms()
        self.nwx_mols = {
            'H2': mokup.get_molecule(mokup.molecule.h2),
            'H2_2': mokup.get_molecule(mokup.molecule.h2_2),
            'H2O': mokup.get_molecule(mokup.molecule.h2o)
        }
        self.pyscf_mols = {
            'H2': gto.M(atom=geoms['H2'], unit='B'),
            'H2_2': gto.M(atom=geoms['H2_2'], unit='B'),
            'H2O': gto.M(atom=geoms['H2O'], unit='B')
        }

    def test_convert_to_pyscf(self):
        '''Tests convert_to_pyscf without providing a Mole object.

        These unit tests check that the conversions from neutral, anionic, and
        cationic systems behave correctly. The underlying implementation relies
        on ``molecule_conversion.convert_to_pyscf``, which is tested elsewhere
        (and assumed to work). In turn we really only need to test that the
        charge and spin are set correctly.
        '''

        for mol_name, mol in self.nwx_mols.items():
            # Test the neutral system
            neutral = chemist.ChemicalSystem(mol)
            pyscf_mol = convert_to_pyscf(neutral)
            corr = self.pyscf_mols[mol_name]
            compare_pyscf_mol(self, pyscf_mol, corr)

            # Test the system with an extra electron (minus one charge)
            n_e_plus_1 = neutral.nelectrons() + 1
            charged = chemist.ChemicalSystem(mol, n_e_plus_1)
            pyscf_mol = convert_to_pyscf(charged)
            corr.charge = -1
            corr.spin = 1
            corr.build()
            compare_pyscf_mol(self, pyscf_mol, corr)

            # Test the system with one less electron (plus one charge)
            n_e_minus_1 = neutral.nelectrons() - 1
            charged = chemist.ChemicalSystem(mol, n_e_minus_1)
            pyscf_mol = convert_to_pyscf(charged)
            corr.charge = 1
            corr.spin = 1
            corr.build()
            compare_pyscf_mol(self, pyscf_mol, corr)

        def test_convert_to_pyscf_with_mole_object(self):
            '''Tests convert_to_pyscf when a Mole object is provided.

            This unit test is similar to ``test_convert_to_pyscf`` except that
            we provide an already initialized Mole object. Here we set
            ``verbose = 5`` on the input and check that ``verbose = 5`` is also
            set on the output as a means of verifying that the function only
            modifies the atomic identities, coordinates, charge, and spin of
            the input. That the aforementioned state is modified correctly is
            tested in ``test_convert_to_pyscf`` (and in unit tests of the
            subfunctions).
            '''

            for mol_name, mol in self.nwx_mols.items():

                # Test the system with an extra electron (minus one charge)
                neutral = chemist.ChemicalSystem(mol)
                n_e_plus_1 = neutral.nelectrons() + 1
                charged = chemist.ChemicalSystem(mol, n_e_plus_1)
                pyscf_mol = gto.Mole()
                pyscf_mol.verbose = 5
                pyscf_mol = convert_to_pyscf(charged, pyscf_mol)
                corr.charge = -1
                corr.spin = 1
                corr.build()
                compare_pyscf_mol(self, pyscf_mol, corr)
                self.assertEqual(pyscf_mol.verbose, 5)


if __name__ == '__main__':
    unittest.main()
