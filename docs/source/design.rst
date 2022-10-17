#################
FriendZone Design
#################

This page details some of the decisions made in designing FriendZone.

***********************
FriendZone Architecture
***********************

FriendZone is meant to be a single NWChemEx plugin. This is because:

- Relatively speaking, wrapping an additional backend requires a fairly minor
  amounts of code. Making new repositories for each backend is thus overkill.
- Some of the conversion infrastructure can be reused, *e.g.*, many backends
  expect inputs in XYZ format so the conversion from a ``Chemist::Molecule``
  to XYZ format can be reused.

FriendZone is written as a Python package:

- Many third party electronic structure packages provide Python support.
- Driving backends which rely on the traditional input script/executable model
  is easier from Python than C++.

The Python package implementing FriendZone is comprised of sub-packages.
Each sub-package is responsible for providing PluginPlay::Modules for one
backend (when the PluginPlay::Modules are backend specific) or for all
backends which share a common API (*e.g.*, one sub-pacakge for interfacing
with backends which support QCSchema). This decision stems from:

- Organization. Putting all of, say, PySCF's bindings together offers a logical
  separation of content.
- Ease of optional support. If down the road we want to make support for a
  specific backend optional it is easier to do this at a Python package
  level than by picking and choosing individual Python modules.
