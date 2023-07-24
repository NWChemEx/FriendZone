from pluginplay import ModuleManager
from friendzone import friends,load_modules
from simde import Energy
from molecules import make_h2
import unittest

class TestNWChem(unittest.TestCase):
    def test_scf(self):
        mol = make_h2()
        key = 'NWChem : SCF'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(Energy(), key, mol)
        self.assertAlmostEqual(egy, -1.094184522864, places=5)


    def test_mp2(self):
        mol = make_h2()
        key = 'NWChem : mp2'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(Energy(), key, mol)
        self.assertAlmostEqual(egy, -1.111247857166, places=5)


    def test_ccsd(self):
        mol = make_h2()
        key = 'NWChem : ccsd'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(Energy(), key, mol)
        self.assertAlmostEqual(egy, -1.122251361965036, places=5)


    def test_ccsd_t(self):
        mol = make_h2()
        key = 'NWChem : ccsd(t)'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(Energy(), key, mol)
        self.assertAlmostEqual(egy, -1.122251361965036, places=5)


    def setUp(self):
        if not friends.is_friend_enabled('nwchem'):
            self.skipTest("NWChem backend is not enabled!")

        self.mm = ModuleManager()
        load_modules(self.mm)