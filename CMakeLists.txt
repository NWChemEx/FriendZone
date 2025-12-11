# Copyright 2022 NWChemEx-Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.14)

#Downloads common CMake modules used throughout NWChemEx
include(cmake/get_nwx_cmake.cmake)

#Sets the version to whatever git thinks it is
include(get_version_from_git)
get_version_from_git(friendzone_version "${CMAKE_CURRENT_LIST_DIR}")
project(friendzone VERSION "${friendzone_version}" LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

include(get_cmaize)
include(nwx_cxx_api_docs)

### Files and Paths ###
set(python_src_directory "${CMAKE_CURRENT_LIST_DIR}/src/python")

# # Doxygen docs
nwx_cxx_api_docs("${CMAKE_CURRENT_SOURCE_DIR}/src" "${CMAKE_CURRENT_SOURCE_DIR}/include")

### Options ###
cmaize_option_list(
    BUILD_TESTING OFF "Should we build the tests?"
    BUILD_PYBIND11_PYBINDINGS ON "Use Pybind11 to build Python bindings?"
    ENABLE_NWCHEM ON "Should we build support for friend: NWChem ?"
    ENABLE_MOLSSI ON "Build support for the MolSSI interface?"
    ENABLE_ASE ON "Build support for the Atomic Simulation Environment?"
)

## Build FriendZone's dependencies ##
cmaize_find_or_build_dependency(
    simde
    URL github.com/NWChemEx/SimDE
    BUILD_TARGET simde
    FIND_TARGET nwx::simde
    CMAKE_ARGS BUILD_TESTING=OFF
               BUILD_PYBIND11_PYBINDINGS=${BUILD_PYBIND11_PYBINDINGS}
)

## Get the CMake utilities for this project ##
set(
    CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${PROJECT_SOURCE_DIR}/cmake"
    CACHE STRING "" FORCE
)

## Find friends ##
include(ase)
include(molssi)
include(nwchem)

#TOOD: Replace cmaize_add_library when it supports Python
add_library(${PROJECT_NAME} INTERFACE)
target_link_libraries(${PROJECT_NAME} INTERFACE simde)

if("${BUILD_TESTING}")
    include(CTest)
    include(nwx_pybind11)
    set(PYTHON_TEST_DIR "${CMAKE_CURRENT_LIST_DIR}/tests/python")

    nwx_pybind11_tests(
        py_${PROJECT_NAME}
        "${PYTHON_TEST_DIR}/unit_tests/test_friendzone.py"
        SUBMODULES simde chemist pluginplay parallelzone tensorwrapper
    )
endif()

install(
    DIRECTORY "${python_src_directory}/friendzone"
    DESTINATION "${NWX_MODULE_DIRECTORY}"
)
