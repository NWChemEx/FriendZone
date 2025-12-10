<!--
  ~ Copyright 2022 NWChemEx-Project
  ~
  ~ Licensed under the Apache License, Version 2.0 (the "License");
  ~ you may not use this file except in compliance with the License.
  ~ You may obtain a copy of the License at
  ~
  ~ http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
-->

FriendZone
==========

[![Nightly Workflow](https://github.com/NWChemEx/FriendZone/actions/workflows/nightly.yaml/badge.svg)](https://github.com/NWChemEx/FriendZone/actions/workflows/nightly.yaml)

[Documentation](https://nwchemex.github.io/FriendZone)

Provides SimDE compatible APIs so that NWChemEx can play nicely with its
friends, *i.e.*, this repo wraps existing electronic structure packages in
modules so they can be called as submodules in NWChemEx.

# Friends

Packages supported through FriendZone include:
- NWChem

# Warnings
Existing packages come with a lot of different licenses. At the moment we only
consider interfaces to packages that have licenses compatible with
[SimDE](https://github.com/NWChemEx/SimDE) (and
[NWChemEx](https://github.com/NWChemEx/NWChemEx)).

Many of the other packages are by default configured/called suboptimally and
thus the modules in this repo should **NOT** be used for direct timing
comparisons unless otherwise noted. Performance contributions are greatly
appreciated.

# Installation

As with the majority of the NWChemEx stack, FriendZone uses CMake and the
[CMaize](https://github.com/CMakePP/CMaize) library for configuration and
building. This means that installation is usually achieved via a variation on:

```.sh
git clone https://github.com/NWChemEx/FriendZone
cd FriendZone
cmake -H. -Bbuild -D...
cmake --build build --target install
```
More detailed install instructions can be found
[here](https://nwchemex.github.io/FriendZone/installation.html).

# Contributing

- [Contributor Guidelines](https://github.com/NWChemEx/.github/blob/1a883d64519f62da7c8ba2b28aabda7c6f196b2c/.github/CONTRIBUTING.md)
- [Contributor License Agreement](https://github.com/NWChemEx/.github/blob/master/.github/CONTRIBUTING.md#contributor-license-agreement-cla)
- [Developer Documentation](https://nwchemex.github.io/FriendZone/developer/index.html)
- [Code of Conduct](https://github.com/NWChemEx/.github/blob/master/.github/CODE_OF_CONDUCT.md)

# Acknowledgments

This research was supported by the Exascale Computing Project (17-SC-20-SC), a
collaborative effort of the U.S. Department of Energy Office of Science and the
National Nuclear Security Administration.
