from friendzone.nwx2qcengine.chemical_system2qc_mol import *
from molecules import make_h2
import qcelemental as qcel
import unittest

class TestChemicalSystem2QC(unittest.TestCase):
    def test_h2(self):
        mol = make_h2()
        qcel_mol = chemical_system2qc_mol(mol)

        h2_as_str = "H 0.0 0.0 0.0\nH 0.0 0.0 0.8899966917653396"
        corr = qcel.models.Molecule.from_data(h2_as_str)
        self.assertEqual(qcel_mol, corr)
