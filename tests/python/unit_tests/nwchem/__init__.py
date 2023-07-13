from pluginplay import pluginplay
from friendzone import load_modules
from simde import Energy
from ..molecules import make_h2
import unittest

def TestNWChem(unittest.TestCase):
    def test_scf(self):
        mol = make_h2()
        key = 'NWChem : SCF'
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(Energy(), key, mol)
        print(egy)


    def setUp(self):
        self.mm = ModuleManager()
        load_modules(self.mm)
