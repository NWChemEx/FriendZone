.. Copyright 2023 NWChemEx-Project
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.

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
