# import unittest
# from pyscf import gto
# from friendzone.pyscf.molecule_conversions import (convert_to_pyscf,
#                                                    convert_from_pyscf)
# from mokup import mokup
# from .test_pyscf import compare_pyscf_mol, string_geoms


# class TestMoleculeConversions(unittest.TestCase):
#     '''Tests functionality found in the friendzone.pyscf.molecule_conversions
#     module.

#     :param nwx_mols: A dictionary mapping molecule names to geometries. The
#         geometries are in the format specified in Chemist.
#     :type nwx_mols: dict(str, chemist.Molecule)

#     :param pyscf_mols: A dictionary mapping molecule names to PySCF inputs. The
#         inputs are initialized to a state consistent with calling
#         ``molecule_conversions.convert_to_pyscf`` and are used as the correct
#         answers.
#     :type pyscf_mols: dict(str, pyscf.gto.Mole)
#     '''

#     def setUp(self):
#         '''Initializes the attributes.'''
#         geoms = string_geoms()
#         self.nwx_mols = {
#             'H2': mokup.get_molecule(mokup.molecule.h2),
#             'H2_2': mokup.get_molecule(mokup.molecule.h2_2),
#             'H2O': mokup.get_molecule(mokup.molecule.h2o)
#         }
#         self.pyscf_mols = {
#             'H2': gto.M(atom=geoms['H2'], unit='B'),
#             'H2_2': gto.M(atom=geoms['H2_2'], unit='B'),
#             'H2O': gto.M(atom=geoms['H2O'], unit='B')
#         }

#     def test_convert_to_pyscf(self):
#         '''Tests convert_to_pyscf without providing a Mole object'''
#         for mol_name, mol in self.nwx_mols.items():
#             pyscf_mol = convert_to_pyscf(mol)
#             corr = self.pyscf_mols[mol_name]
#             compare_pyscf_mol(self, pyscf_mol, corr)

#     def test_convert_to_pyscf_no_default(self):
#         '''Tests convert_to_pyscf by providing a Mole object

#         ``test_convert_to_pyscf`` relied on ``convert_to_pyscf`` intializing
#         the return value. This unit test instead uses an already initialized
#         PySCF Mole object. The previous test ensured that the resulting object
#         is set up correctly, here we make sure that ``convert_to_pyscf`` only
#         modifies the appropriate state by setting the spin before calling
#         ``convert_to_pyscf``.
#         '''
#         for mol_name, mol in self.nwx_mols.items():
#             pyscf_mol = gto.Mole()
#             pyscf_mol.spin = 2
#             pyscf_mol = convert_to_pyscf(mol, pyscf_mol)
#             corr = self.pyscf_mols[mol_name]
#             corr.spin = 2

#             # Make sure spin is unchanged
#             self.assertEqual(pyscf_mol.spin, 2)

#             # Compare the rest of the state
#             compare_pyscf_mol(self, pyscf_mol, corr)

#     def test_convert_from_pyscf(self):
#         '''Tests converting back from a PySCF Mole object.'''
#         for mol_name, mol in self.pyscf_mols.items():
#             nwx_mol = convert_from_pyscf(mol)
#             corr = self.nwx_mols[mol_name]

#             # Ensure same number of atoms
#             self.assertEqual(nwx_mol.size(), corr.size())

#             # Compare atoms
#             for atom_i, corr_i in zip(nwx_mol, corr):
#                 # Compare atomic number
#                 self.assertEqual(atom_i.Z(), corr_i.Z())

#                 # Compare coords
#                 for q in range(3):
#                     self.assertAlmostEqual(atom_i[q], corr_i[q])


# if __name__ == '__main__':
#     unittest.main()
