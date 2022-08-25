from pyscf import gto
from simde import chemist


def convert_to_pyscf(nwx_mol, pyscf_mol=None):
    """ Converts a chemist.Molecule instance into a PySCF Mole object.

    PySCF's Mol object contains state that in NWChemEx is spread out across a
    number of classes (*e.g.*, ChemicalSystem, Molecule, and AOSpace). This
    function fills in the part of the PySCF object which comes from NWChemEx's
    Molecule object. Since PySCF's object has additional state, users may
    optionally pass in an already existing PySCF object and this function will
    just change the Molecule part of the input, leaving all other state
    untouched.

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

    if pyscf_mol == None:
        pyscf_mol = gto.Mole()

    pyscf_mol.unit = 'B'
    atoms = ''
    atom_counts = {}

    for atom_i in nwx_mol:
        z = atom_i.Z()
        sym = atom_i.name()
        if z in atom_counts:
            atom_counts[z] += 1
        else:
            atom_counts[z] = 0

        sym += str(atom_counts[z])
        carts = atom_i.coords()
        atom_str = '{} {:.16f} {:.16f} {:.16f};'.format(
            sym, carts[0], carts[1], carts[2])
        atoms += atom_str

    # Remove trailing ';'
    atoms = atoms[:-1]
    print(atoms)
    pyscf_mol.atom = atoms
    pyscf_mol.build()
    return pyscf_mol


def convert_from_pyscf(pyscf_mol):
    """ Converts a PySCF Mole object into a Chemist Molecule object

    :param pyscf_mol: The Mole object we are converting from
    :type pyscf_mol: pyscf.gto.Mole

    :return: The Chemist Molecule object with atoms populated from ``pyscf_mol``
    :rtype: chemist.Molecule
    """

    nwx_mol = chemist.Molecule()

    for i in range(pyscf_mol.natm):
        py_z = pyscf_mol.atom_charge(i)
        Z = chemist.Atom.AtomicNumber(int(py_z))
        sym = pyscf_mol.atom_pure_symbol(i)
        carts = pyscf_mol.atom_coord(i, 'Bohr')
        r = chemist.Atom.coord_type([float(carts[q]) for q in range(3)])
        nwx_mol.push_back(chemist.Atom(sym, Z, r))

    return nwx_mol
