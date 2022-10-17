'''Functions to facilitate testing ``friendzone.nwx_pyscf``

The functions in this module focus on generating hard-coded state and comparing
PySCF Mole instances.
'''


def string_geoms():
    '''This function returns the geometries stored in Mokup, in a string format
    suiatable for use as input to PySCF.

    The result has the following entries:

    1. ``'H2'`` a hydrogen molecule
    2. ``'H2_2'`` two hydrogen molecules separated by 40 bohr
    3. ``'H2O'`` a water molecule
    4. ``'H2(H2)'`` the ``'H2_2'`` system, but with ghost atoms where
       the second hydrogen molecule would be.

    :return: A dictionary whose keys are the molecule names and the values are
        the geometry.
    :rtype: dictionary(str, str)
    '''
    return {
        'H2':
        'H0 0.0 0.0 0.0; H1 0.0 0.0 1.6818473865225443',
        'H2_2':
        '''
            H0 0.0 0.0  0.0
            H1 0.0 0.0  1.6818473865225443
            H2 0.0 0.0 41.6818473865225443
            H3 0.0 0.0 43.363694773
            ''',
        'H2O':
        '''
            O0  0.0               -0.143222342980786 0.0
            H0  1.638033502034240  1.136556880358410 0.0
            H1 -1.638033502034240  1.136556880358410 0.0
            ''',
        'H2(H2)':
        '''
        H0 0.0 0.0  0.0
        H1 0.0 0.0  1.6818473865225443
        ghost_H0 0.0 0.0 41.6818473865225443
        ghost_H1 0.0 0.0 43.363694773
        '''
    }


def compare_pyscf_mol(test_case, pyscf_mol, corr):
    ''' Compares the molecule part of two pyscf.gto.Mole objects.

    AFAIK PySCF does not have a way to compare Mol instances, so
    we wrote this function. This function compares the molecule part of
    the Mol objects, which we define as:

    - Number of atoms
    - Unit for coordinates (*i.e.*, Bohr or Angstroms)
    - Charge
    - Spin
    - Atomic symbols
    - Nuclear charge
    - Cartesian coordinates

    .. note::

       The names of the arguments are logical only, permuting ``pyscf_mol``
       and ``corr`` will result in the same behavior.

    :param pyscf_mol: The molecule we generated
    :type pyscf_mol: pyscf.gto.Mole
    :param corr: The reference instance to compare against
    :type corr: pyscf.gto.Mole
    '''

    # Ensure same number of atoms
    test_case.assertEqual(pyscf_mol.natm, corr.natm)

    # Ensure same units
    test_case.assertEqual(pyscf_mol.unit, corr.unit)

    # Ensure same charge
    test_case.assertEqual(pyscf_mol.charge, corr.charge)

    # Ensure same spin
    test_case.assertEqual(pyscf_mol.spin, corr.spin)

    # Compare the atoms
    for i in range(corr.natm):

        # Ensure same atomic symbol
        test_case.assertEqual(pyscf_mol.atom_symbol(i), corr.atom_symbol(i))

        # Ensure same atomic number
        test_case.assertEqual(pyscf_mol.atom_charge(i), corr.atom_charge(i))

        # Ensure (approximately) the same coordinates
        carts = pyscf_mol.atom_coord(i, 'Bohr')
        corr_carts = corr.atom_coord(i, 'Bohr')
        for q in range(3):
            test_case.assertAlmostEqual(carts[q], corr_carts[q])


def compare_pyscf_basis(test_case, mol, corr):
    ''' Compares the AO basis set part of two pyscf.gto.Mole objects.

    AFAIK PySCF does not have a way to compare Mol instances, so
    we wrote this function to compare the AO basis set part of two Mol
    instances. We define the AO basis set part as:

    - Number of atoms (overlaps with ``compare_pyscf_mol``)
    - Number of shells per atom
    - Angular momentum of each shell
    - The number of primitives in each shell
    - Contraction coefficients of each primitive
    - Exponents of each primitive

    .. note::

       The names of the arguments are logical only, permuting ``mol``
       and ``corr`` will result in the same behavior.

    :param mol: The molecule we generated
    :type mol: pyscf.gto.Mole
    :param corr: The reference instance to compare against
    :type corr: pyscf.gto.Mole
    '''

    # Ensure same number of atoms
    n_atoms = mol.natm
    test_case.assertEqual(n_atoms, corr.natm)

    for atom in range(n_atoms):
        n_shells = mol.atom_nshells(atom)

        # Ensure same number of shells
        test_case.assertEqual(n_shells, corr.atom_nshells(atom))

        for shell in range(n_shells):
            # Ensure same angular momentum
            l = mol.bas_angular(shell)
            corr_l = corr.bas_angular(shell)
            test_case.assertEqual(l, corr_l)

            # Ensure (approximately) equal coefficients
            coefs = mol.bas_ctr_coeff(shell)
            corr_coefs = corr.bas_ctr_coeff(shell)
            test_case.assertEqual(len(coefs), len(corr_coefs))
            for c_i, corr_c_i in zip(coefs, corr_coefs):
                test_case.assertAlmostEqual(c_i, corr_c_i)

            # Ensure (approximately) equal exponents
            alpha = mol.bas_exp(shell)
            corr_alpha = corr.bas_exp(shell)
            test_case.assertEqual(len(alpha), len(corr_alpha))
            for a_i, corr_a_i in zip(alpha, corr_alpha):
                test_case.assertAlmostEqual(a_i, corr_a_i)
