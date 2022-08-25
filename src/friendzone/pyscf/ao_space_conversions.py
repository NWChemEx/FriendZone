from pyscf import gto
from simde import chemist

# N.B. I'm not sure if we really ever need to convert PySCF's basis back to NWX
# so I skipped that conversion for now.


def convert_to_pyscf(nwx_ao_space, atom2center, pyscf_mol):
    """Adds the state of an NWChemEx AOSpace to a PySCF Mole object.

    Notes on implementation
    =======================
    - In probably 99% of cases we could "cheat" and use atomic basis set
      names (*e.g.*, STO-3G, cc-pVDZ); however, there's no guarantees that:

        1. the creator of the NWChemEx basis set tagged it right, and
        2. PySCF agrees on the parameters of the basis set
    - Again, in probably 99% of cases atomic basis sets are set per atom type,
      *e.g.*, all carbons share the same AO parameters. This means we probably
      could set the parameters once. However, this involves floating point
      comparisons on our side (to ensure that the parameters really are the
      same) which we want to avoid. It's not clear that it saves us anything
      anyways since under the hood the parameters are probably just set per
      atom anyways.
    - Unfortunately PySCF's public API for setting the basis set is string
      based, so this routine builds up a string representation of the basis
      set in ``nwx_ao_space`` to pass it to PySCF

    :param nwx_ao_space: The NWChemEx AOSpace whose state is being added to
        ``pyscf_mol``.
    :type nwx_ao_space: chemist.orbital_space.AOSpaceD
    :param pyscf_mol: The PySCF

    :return: ``pyscf_mol``, but now with an AO basis set.
    :rtype: pyscf.gto.Mole
    """

    # Assume pyscf_mol has the atoms already (correctly) set. In that case
    # atom2center better agree with pyscf_mol on the number of atoms
    assert len(atom2center) == pyscf_mol.natm

    # We have ghost atoms if nwx_ao_space.size() != pyscf_mol.natm.
    n_atoms = pyscf_mol.natm
    n_ao_centers = nwx_ao_space.size()

    # This is used to convert the integer angular momentum values
    am = 'spdfghijklmno'

    # This will be the basis set in string format
    # The format we're after looks like:
    #
    # <Atomic Symbol> <Letter for Angular Momentum>
    #     <exponent 0> <coefficient 0>
    #     <exponent 1> <coefficient 1>
    #
    # repeated for each shell.
    bs = {}

    for atom, center in enumerate(atom2center):
        nwx_center = nwx_ao_space.basis_set()[center]
        sym = pyscf_mol.atom_pure_symbol(atom)

        bs_str = ""
        for shell in nwx_center:
            bs_str += "{} {}\n".format(sym, am[shell.l()])
            for prim_i in range(shell.n_unique_primitives()):
                prim = shell.unique_primitive(prim_i)
                alpha = prim.exponent()
                c = prim.coefficient()
                bs_str += "{:.16f} {:.16f}\n".format(alpha, c)

        bs[pyscf_mol.atom_symbol(atom)] = gto.basis.parse(bs_str)

    pyscf_mol.basis = bs
    pyscf_mol.build()
    return pyscf_mol
