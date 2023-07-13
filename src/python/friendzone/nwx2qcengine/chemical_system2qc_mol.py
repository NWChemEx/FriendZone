import qcelemental as qcel

def chemical_system2qc_mol(chem_sys):
    """ Converts a chemist.ChemicalSystem object into a QCElemental.Molecule

        At present there is far more information in the input chemical system
        then in the output object. In particular, our implementation only
        worries about:

        - Chemical symbols
        - Cartesian coordinates (including the Bohr to angstrom conversion)
    """

    out = ""
    mol = chem_sys.molecule
    au2ang = qcel.constants.conversion_factor("bohr", "angstrom")
    for i in range(mol.size()):
        atom_i = mol.at(i)
        symbol = atom_i.name
        x      = str(atom_i.x * au2ang)
        y      = str(atom_i.y * au2ang)
        z      = str(atom_i.z * au2ang)
        out += symbol + " " + x + " " + y + " " + z + "\n"
    return qcel.models.Molecule.from_data(out)
