def compare_pyscf_mol(test_case, pyscf_mol, corr):
    ''' AFAIK PySCF does not have a way of comparing Mol instances, so
    we wrote this function. N.B., the names of the arguments are logical
    only, permuting the reference and the object being checked will generate
    the same result.

    :param pyscf_mol: The molecule we generated
    :type pyscf_mol: pyscf.gto.Mole
    :param corr: The reference instance to compare against
    :type corr: pyscf.gto.Mole
    '''

    # Ensure same number of atoms
    test_case.assertEqual(pyscf_mol.natm, corr.natm)

    # Ensure same units
    test_case.assertEqual(pyscf_mol.unit, corr.unit)

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
            for c_i, corr_c_i in zip(coefs, corr_coefs):
                test_case.assertAlmostEqual(c_i, corr_c_i)

            # Ensure (approximately) equal exponents
            alpha = mol.bas_exp(shell)
            corr_alpha = corr.bas_exp(shell)
            for a_i, corr_a_i in zip(alpha, corr_alpha):
                test_case.assertAlmostEqual(a_i, corr_a_i)
