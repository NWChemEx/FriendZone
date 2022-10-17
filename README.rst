##########
FriendZone
##########

Provides SimDE compatible APIs so that NWChemEx can play nicely with its
friends, *i.e.*, this repo wraps existing electronic structure packages in
modules so they can be called as submodules in NWChemEx.

.. warning::

   Existing packages come with a lot of different licenses. At the moment we
   only consider interfaces to packages that have licenses compatible with
   SimDE (and NWChemEx).

.. warning::

   Many of the other packages are by default configured/called suboptimally
   and thus the modules in this repo should **NOT** be used for direct
   timing comparisons unless otherwise noted. Performance contributions
   are greatly appreciated.
