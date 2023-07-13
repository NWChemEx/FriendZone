from chemist import Atom, Molecule, ChemicalSystem

def make_h2():
    mol = Molecule()
    mol.push_back(Atom('H', 1, 1839.0, 0.0, 0.0, 0.0))
    mol.push_back(Atom('H', 1, 1839.0, 0.0, 0.0, 1.68185))

    return ChemicalSystem(mol)
