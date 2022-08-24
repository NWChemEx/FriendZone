import friendzone as fz
from simde import simde, chemist

mol = chemist.Molecule()
pyscf_mol = fz.pyscf.convert_mol_to_pyscf(mol)
print(pyscf_mol)
