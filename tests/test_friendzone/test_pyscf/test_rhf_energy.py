# import unittest
# import friendzone.pyscf
# from simde import simde, chemist, pluginplay
# from mokup import mokup

# class TestRHFEnergy(unittest.TestCase):
#     '''Tests functionality found in the friendzone.pyscf.rhf_energy module.

#     :param molecules: A list of molecules to run
#     :type molecules: list(mokup.molecule)

#     :param bs: A list of basis sets to run
#     :type bs: list(mokup.basis_set)

#     :param corr: Map from molecule-basis set pairs to its total SCF energy.
#     :type corr: dict(tuple(mokup.molecule, mokup.basis_set), float)
#     '''

#     def setUp(self):
#         '''Initializes the attributes.'''

#         h2 = mokup.molecule.h2
#         h2_2 = mokup.molecule.h2_2
#         h2o = mokup.molecule.h2o
#         sto3g = mokup.basis_set.sto3g

#         self.molecules = [h2, h2_2, h2o]
#         self.bs = [sto3g]
#         self.corr = {
#             (h2, sto3g): -1.09418483235277,
#             (h2_2, sto3g): -2.1883696566775592,
#             (h2o, sto3g): -74.9420800589486
#         }

#     def test_rhf_energy(self):
#         '''Tests the run member of the RHFEnergy class.

#         This unit test loops over all molecule-basis set pairs, computes the
#         SCF energy of the input, and then compares the energy to the reference
#         values.
#         '''

#         mm = pluginplay.ModuleManager()
#         friendzone.pyscf.load_modules(mm)

#         for m_mol in self.molecules:
#             for m_aos in self.bs:
#                 mol = mokup.get_molecule(m_mol)
#                 sys = chemist.ChemicalSystem(mol)
#                 aos = mokup.get_bases(m_mol, m_aos)

#                 [e] = mm.at("PySCF RHF").run_as[simde.AOEnergy](aos, sys)
#                 self.assertAlmostEqual(e, self.corr[(m_mol, m_aos)], places=5)

# if __name__ == '__main__':
#     unittest.main()
