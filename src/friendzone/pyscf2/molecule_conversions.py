from pyscf import gto
from simde import chemist


def convert_to_pyscf(nwx_mol, pyscf_mol = gto.Mole()):
    """ Converts a chemist.Molecule instance into a PySCF Mole object.

    :param nwx_mol: The Molecule object we are converting from
    :type nwx_mol: chemist.Molecule
    :param pyscf_mol: The user can optionally specify an already existing
        PySCF Mole instance and this function will populate the ``atoms``
        member of the provided instance instead of creating a new PySCF Mole
        instance.
    :type pyscf_mol: pyscf.gto.Mole, optional

    :return: The PySCF Mole object whose atoms are populated from ``nwx_mol``
    :rtype: pyscf.gto.Mole
    """

    pyscf_mol.unit = 'B'
    atoms = []

    for atom_i in nwx_mol:
        sym = atom_i.Z()
        carts = [atom_i.coords()[i] for i in range(3)]
        atoms.append([sym, carts])

    pyscf_mol.atom = atoms

    return pyscf_mol


def convert_from_pyscf(pyscf_mol, nwx_mol = chemist.Molecule()):

    for atom_i in pyscf_mol.atom:
        Z = chemist.Atom.AtomicNumber(atom_i[0])
        r = chemist.Atom.coord_type([atom_i[1][i] for i in range(3)])
        nwx_mol.push_back(chemist.Atom(Z, r))

    return nwx_mol
