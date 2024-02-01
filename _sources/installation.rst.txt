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

.. _installing_fz:

############
Installation
############

******************************************
Step 0: Setup a Python Virtual Environment
******************************************

FriendZone interacts with its friends through Python. We thus highly recommend
(and this tutorial will assume) that you setup a Python virtual environment
prior to installing anything. This is done by:

.. code-block:: bash

   python -m venv my_venv
   source my_venv/bin/activate

Here ``my_venv`` is the name of the virtual environment you are creating (feel
free to change this). The above commands will create a virtual environment
``my_venv`` which lives in the directory you run the commands in (Python
virtual environments are simply directories) and activate it (which makes that
the Python installation used until the environment is deactivated, which is
done by running the appropriately named command ``deactivate``).

***************************************
Step 1: Install FriendZone Dependencies
***************************************

FriendZone depends on `SimDE <https://github.com/NWChemEx/SimDE>`__,
several Python modules, and whatever friends (*i.e.*, other electronic structure
packages) you want to enable. FriendZone's build system can build and install
SimDE for you (if it is not found), but at present it can not install the Python
modules or friends.

To install the Python module dependencies into the virtual environment from
Step 0 (so assuming it is still activated) simply run the following in the
root directory of FriendZone:

.. code-block:: bash

   pip install -r requirements.txt

The installation instructions for each friend can vary widely and we have
dedicated the entire :ref:`how_to_install_our_various_friends` section below
to this topic.

**************************
Step 2: Install FriendZone
**************************

Once the dependencies are installed, FriendZone can be built using the usual
CMake commands:

.. code-block:: bash

   cmake -H. \
         -B<build_dir> \
         -DCMAKE_INSTALL_PREFIX:PATH=<where/to/install/libraries> \
         -DCMAKE_TOOLCHAIN_FILE:PATH=<path/to/toolchain.cmake>
   cmake --build build --target install --parallel 2

Here ``<build_dir>`` is the name of the build directory CMake should use (most
users just set this to ``-Bbuild``), ``<where/to/install/libraries>`` should
be set to where you want to install the dependencies FriendZone builds for you,
and ``<path/to/toolchain.cmake>`` should point to your ``toolchain.cmake`` file.
Of particular note, make sure that in your toolchain file you set
``NWX_MODULE_PATH`` to where you want FriendZone installed and you may want to
set both ``Python_EXECUTABLE`` and ``Python3_EXECUTABLE`` to the Python
interpreter from your virtual environment (with the environment activated
run ``which python3`` to get it's path).

********************************
Step 3: Play Nicely with Friends
********************************

Once FriendZone is installed you should be able to just include
``NWX_MODULE_PATH`` in your ``PYTHONPATH`` and be able to use it!


.. _how_to_install_our_various_friends:

**********************************
How to Install Our Various Friends
**********************************

NWChem
======

Full instructions can be
found `here <https://nwchemgit.github.io/Download.html>`__.

The easiest way to install NWChem (although such an installation is unlikely
to be high-performance) is via a package manager. On Ubuntu/Debian, this
is simply:

.. code-block::

   sudo apt-get install nwchem


For Mac, NWChem can be installed via [Homebrew](https://brew.sh/):

.. code-block::

    brew install nwchem

For performance critical runs, it is strongly recommended that you build NWChem
from source.
