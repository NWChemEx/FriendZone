from pyscf import gto
from simde import chemist
import math

# N.B. I'm not sure if we really ever need to convert PySCF's basis back to NWX
# so I skipped that conversion for now.


def atom_to_ao(pyscf_mol, nwx_ao_space):
    ''' Assigns each atom in ``pyscf_mol`` to a center in ``nwx_ao_space``

    This function assumes that for an atom ``a`` in ``pyscf_mol`` there is one
    center ``c`` that is much closer than all other centers in ``nwx_ao_space``.
    This function assigns center ``c`` to atom ``a``. At this point this
    fucntion does not ensure that ``c`` only gets assigned to one atom or that
    ``c`` is more or less on top of ``a`` (we only know ``c`` is the closest
    center to ``a``).

    :param pyscf_mol: The atoms we are assigning to AO centers.
    :type pyscf_mol: pyscf.gto.Mole
    :param nwx_ao_space: The AOSpace whose centers are being assigned.
    :type nwx_ao_space: chemist.AOSpaceD

    :return: A list such that the ``i``-th element is the center atom ``i``
        maps to.
    :rtype: list(int)

    .. todo::

       This should probably be turned into a module so it can be used elsewhere
       in NWChemEx.
    '''

    rv = []
    bs = nwx_ao_space.basis_set()

    def distance(lhs, rhs):
        '''Comptues distance between two points. Assumes three components'''

        dr2 = [(lhs[i] - rhs[i])**2 for i in range(3)]
        return math.sqrt(dr2[0] + dr2[1] + dr2[2])

    n_centers = bs.size()

    # AOBasisSet has no way to get back an (x, y, z) tuple, so we precompute
    # tuples for each center, those tuples will liev in center_carts
    center_carts = []
    for i in range(n_centers):
        center_carts.append([bs[i].coord(j) for j in range(3)])

    # For each atom our goal is to find the closest center
    for i in range(pyscf_mol.natm):
        atom_carts = pyscf_mol.atom_coord(i, 'Bohr')

        # Here we initialize the current winner to center 0
        winning_distance = distance(atom_carts, center_carts[0])
        winning_center = 0

        # Now we loop over the remaining centers and see if one is closer
        for j in range(1, n_centers):
            d2j = distance(atom_carts, center_carts[j])

            # Is center j closer than our current winner?
            if d2j < winning_distance:
                winning_distance = d2j
                winning_center = j

        # We now know the winner, append it
        rv.append(winning_center)

    return rv


def convert_to_pyscf(nwx_ao_space, atom2center, pyscf_mol):
    '''Adds the state of an NWChemEx AOSpace to a PySCF Mole object.

    :param nwx_ao_space: NWChemEx represents AOs via the AOSpace object. This
        class is conceptually a container of AtomicBasisSet objects (each of
        which represent a set of AOs on a common center). ``nwx_ao_space`` is
        the NWChemEx AOSpace object we are using to populate the basis set of
        the ``pyscf_mol`` object
    :type nwx_ao_space: chemist.AOSpaceD

    :param atom2center: A list such that ``atom2center[i]`` is the offset of
        the AtomicBasisSet (*i.e.*, element of ``nwx_ao_space``) for the
        ``i``-th atom in ``pyscf_mol``. *N.B*, NWChemEx does not count ghost
        atoms as atoms, so  ``len(atom2center)`` may be less than the number
        of centers in ``nwx_ao_space``.
    :type atom2center: list(int)

    :param pyscf_mol: This is the input to PySCF we are adding an AO basis set
        to. It is assumed that each atom has a unique symbol (*e.g.*, the
        first hydrogen atom is "H0", the second is "H1", etc.). Using
        molecule_conversions.convert_to_pyscf will satisfy this assumption
        automatically.
    :type pscf_mol: pyscf.gto.Mole

    :return: ``pyscf_mol`` after adding the AO basis set found in
        ``nwx_ao_space`` to it.
    :rtype: pyscf.gto.Mole

    :raises AssertionError: If the number of atoms in ``pyscf_mol`` is not
        equal to the length of ``atom2center`` or if the number of centers
        in ``atom2center`` is less than the number of atoms in ``pyscf_mol``.
    :raises KeyError: If a center is assigned to more than one atom or if an
        element of ``atom2center`` is greater than or equal to
        ``len(nwx_ao_space)``

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

    Basis Set Format
    ----------------

    Unfortunately PySCF's public API for setting the basis set is string
    based, so this routine builds up a string representation of the basis
    set in ``nwx_ao_space`` to pass it to PySCF. The format for each
    shell is:

    .. code::

       <Atomic Symbol> <Letter for Angular Momentum>
           <exponent 0> <coefficient 0>
           <exponent 1> <coefficient 1>

    Ghost Atoms
    -----------

    Our ghost atom solution assumes that all centers not present in
    atom2center are ghost atoms. It gets a bit hacky from there, but we do the
    best we can given that AFAIK PySCF forces us to assign atomic numbers to
    ghost atoms. For geometry specification, PySCF lets us do something like:

    .. code::

       ghost_H 0.0 0.0 0.0

    to define a ghost atom, sitting at the origin, which uses hydrogen's basis
    set. By using atom names like ``ghost_H0``, ``ghost_H1``, etc. we can tell
    the ghost atoms apart and more importantly can assign each ghost atom its
    own basis set analogous to how we assigned basis sets for each real atom.
    The only difference is when we generate the basis set string, we always
    use hydrogen as the atomic symbol (the identity of the ghost atom's atomic
    identity is irrelevant for all purposes beyond assigning basis functions).
    '''

    # Assume pyscf_mol has the atoms already (correctly) set. In that case
    # atom2center better agree with pyscf_mol on the number of atoms
    assert len(atom2center) == pyscf_mol.natm

    # We have ghost atoms if nwx_ao_space.size() != pyscf_mol.natm.
    n_atoms = pyscf_mol.natm
    n_ao_centers = nwx_ao_space.size()
    assert n_ao_centers >= n_atoms
    n_ghosts = n_ao_centers - n_atoms

    # This will be the atom symbol to atomic basis set map we give PySCF
    bs = {}

    remaining_centers = {i for i in range(n_ao_centers)}

    def make_bs_str(sym, nwx_center):
        # This is used to convert the integer angular momentum values
        am = 'spdfghijklmno'

        bs_str = ""

        for shell in nwx_center:
            bs_str += '{} {}\n'.format(sym, am[shell.l()])
            for prim_i in range(shell.n_unique_primitives()):
                prim = shell.unique_primitive(prim_i)
                alpha = prim.exponent()
                c = prim.coefficient()
                bs_str += '{:.16f} {:.16f}\n'.format(alpha, c)

        return bs_str

    ############################################################################
    # Step 0: Make AOs for the "real" atoms                                    #
    ############################################################################

    for atom, center in enumerate(atom2center):
        remaining_centers.remove(center)
        sym = pyscf_mol.atom_pure_symbol(atom)
        nwx_center = nwx_ao_space.basis_set()[center]
        bs_str = make_bs_str(sym, nwx_center)
        bs[pyscf_mol.atom_symbol(atom)] = gto.basis.parse(bs_str)

    ############################################################################
    # Step 1: Make AOs for the "ghost" atoms                                   #
    ############################################################################

    for i, center in enumerate(remaining_centers):
        nwx_center = nwx_ao_space.basis_set()[center]
        bs_str = make_bs_str('H', nwx_center)
        sym = 'ghost_H' + str(i)
        x, y, z = nwx_center.x(), nwx_center.y(), nwx_center.z()
        ghost = ';{} {:.16f} {:.16f} {:.16f}'.format(sym, x, y, z)
        pyscf_mol.atom += ghost
        bs[sym] = gto.basis.parse(bs_str)

    pyscf_mol.basis = bs
    pyscf_mol.build()
    return pyscf_mol
