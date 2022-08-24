import friendzone as fz
from mokup import mokup

mol = mokup.get_molecule(mokup.molecule.h2)
print(mol)
pyscf_mol = fz.pyscf.molecule_conversions.convert_to_pyscf(mol)
print(pyscf_mol.atom)
