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

***************************************
Step 1: Install FriendZone Dependencies
***************************************

Make sure your Python virtual environment from Step 0 is activated and then
run:

.. code-block:: bash

   pip install -r requirements.txt

Again make sure you are in the same virtual environment you created in step 0

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
be set to where you want to install dependencies FriendZone builds for you, and
``<path/to/toolchain.cmake>`` should point to your ``toolchain.cmake`` file.


********************************
Step 3: Play Nicely with Friends
********************************

Once FriendZone is installed you should be able to just include
``NWX_MODULE_PATH`` in your ``PYTHONPATH`` and be able to use it!
