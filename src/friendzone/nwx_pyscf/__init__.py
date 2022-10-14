'''SimDE compatible bindings to PySCF.

PySCF homepage: `link <https://pyscf.org/index.html>`__

From the homepage:

.. pull-quote::

   `"The Python-based Simulations of Chemistry Framework (PySCF) is an
   open-source collection of electronic structure modules powered by Python.
   The package provides a simple, lightweight, and efficient platform for
   quantum chemistry calculations and methodology development. PySCF can be
   used to simulate the properties of molecules, crystals, and custom
   Hamiltonians using mean-field and post-mean-field methods. To ensure ease
   of extensibility, almost all of the features in PySCF are implemented in
   Python, while computationally critical parts are implemented and
   optimized in C. Using this combined Python/C implementation, the package is
   as efficient as the best existing C or Fortran based quantum
   chemistry programs. In addition to its core libraries, PySCF supports a
   rich ecosystem of Extension modules."`

At this time, the SimDE wrappers in this subpackage primarily focus on wrapping
electronic structure methods such as SCF and MP2.
'''

from . import rhf_energy
from . import rmp2_energy
from simde import simde
from cppyy.gbl.std import make_shared


def load_modules(mm):
    '''Adds all existing PySCF modules to the provided ModuleManager.

    At this time all PySCF modules are ready to run as is and do not require
    the user to set any submodules.

    :param mm: The ModuleManager to add the modules to.
    :type mm: pluginplay.ModuleManager
    '''
    mm.add_module('PySCF RHF', make_shared[rhf_energy.RHFEnergy]())
    mm.add_module('PySCF RMP2', make_shared[rmp2_energy.RMP2Energy]())
