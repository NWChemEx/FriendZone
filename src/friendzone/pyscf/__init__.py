from pyscf import gto
from simde import simde


def convert_mol_to_pyscf(nwx_mol):
    pyscf_mol = gto.Mole()
    atoms = []

    for atom_i in nwx_mol:
        sym = atom_i.symbol()
        carts = [atom_i.coords()[i] for i in range(3)]
        atoms.append([sym, carts])

    pyscf_mol.atom = atoms

    return pyscf_mol
