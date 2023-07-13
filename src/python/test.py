from pluginplay import ModuleManager
from friendzone import load_modules
from friendzone.nwchem import NWChemViaMolSSI
from simde import Energy
from chemist import Atom, Molecule, ChemicalSystem

mm = ModuleManager()
load_modules(mm)

mol = Molecule()
mol.push_back(Atom('H', 1, 1839.0, 0.0, 0.0, 0.0))
mol.push_back(Atom('H', 1, 1839.0, 0.0, 0.0, 1.68185))

sys = ChemicalSystem(mol)
mm.change_input('NWChem : SCF', 'basis set', 'sto-3g')
egy = mm.run_as(Energy(), 'NWChem : SCF', sys)

print(egy)
