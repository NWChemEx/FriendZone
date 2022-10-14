'''Conversions involving chemist.ChemicalSystem and pyscf.gto.Mole

The functions in this module provide infrastructure pertaining to converting
Chemist's ChemicalSpace class to (the molecule part of) PySCF's Mole class.

.. note::

   Right now there are no functions for the reverse procedure (PySCF to
   Chemist). If such methods are needed they can easily be added here.
'''

import pyscf
from . import molecule_conversions


def convert_to_pyscf(sys, mol=None):
    ''' Converts NWChemEx's ChemicalSystem to a PySCF molecule

    This function relies on
    ``friendzone.pyscf.molecule_conversions.convert_to_pyscf`` for
    converting the ``Molecule`` instance in ``sys``. The remainder of this
    function addresses the charge and spin of the system.

    .. todo::

       Spin is presently handled in a somewhat naive manner (by assuming
       high spin). Better treatment requires ChemicalSystem to handle spin
       better.


    :param sys: The NWChemEx ChemicalSystem we are converting.
    :type sys: nwchemex.chemist.ChemicalSystem

    :param mol: If provided this is the PySCF molecule that ``sys``'s state
        should be added to. Defaults to an empty PySCF molecule.
    :type mol: pyscf.gto.Mole

    :return: ``mol`` updated to reflect the state of ``sys``.
    :rtype: pyscf.gto.Mole
    '''

    mol = molecule_conversions.convert_to_pyscf(sys.molecule(), mol)
    mol.charge = sys.charge()

    # For now we take the absolute value of the charge to be the number of
    # unpaired electrons, n, the spin is then n + 1 (but PySCF wants it with 0
    # offset so it's actually just n)
    mol.spin = abs(sys.charge())

    mol.build()
    return mol
