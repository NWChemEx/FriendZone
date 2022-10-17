'''Contains tests associated with the PySCF sub-package of FriendZone.

The test_nwx_pyscf package is set up so that the tests for the
``friendzone.nwx_pyscf.x.py`` module are in the
``test_friendzone.test_nwx_pyscf.test_x.py`` module.
'''
from simde import pluginplay

# This line is here to keep MPI alive across the test suite
mm = pluginplay.ModuleManager()
