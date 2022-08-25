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
