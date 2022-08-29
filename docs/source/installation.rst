.. _installing_fz:

############
Installation
############

.. note::

   These instructions represent the current state of how to get FriendZone up
   and running. As building Python bindings for SimDE becomes easier these
   instructions should become more streamlined.

******************************************
Step 0: Setup a Python Virtual Environment
******************************************

FriendZone's modules are written in Python. So it is a good idea to setup a
Python virtual environment prior to installing anything. This is done by:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

*******************
Step 1: Build SimDE
*******************

FriendZone depends explicitly on SimDE. If you intend to use FriendZone with
modules provided by NWChemEx (*e.g.*, modules for assigning AO basis sets),
you may opt to instead build NWChemEx (which will also build SimDE).
Regardless of whether you decide to build SimDE only, or SimDE + NWChemEx,
you should ensure you build the Python bindings using the Python environment
from step 0.

When you build SimDE (and/or NWChemEx) you will do so in a build directory.
For the sake of these instructions we assume ``${BUILD_DIR}`` is the
absolute path to the build directory. In turn, ``${BUILD_DIR}/Python`` is the
absolute path to the generated Python bindings.


***************************************
Step 2: Install FriendZone Dependencies
***************************************

This is done by running (in the root directory of the FriendZone repo):

.. code-block:: bash

   pip install -r requirements.txt

Again make sure you are in the same virtual environment you created in step 0


********************************
Step 3: Play Nicely with Friends
********************************

Since FriendZone is Python only there's no need to install FriendZone, just
make sure it's in your Python path (along with ``${BUILD_DIR}/Python``).
