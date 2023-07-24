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
set(VERSION 1.0.0) #TODO: get from git
project(friendzone VERSION "${VERSION}" LANGUAGES CXX)

include(FetchContent)
FetchContent_Declare(
    nwx_cmake
    GIT_REPOSITORY https://github.com/NWChemEx-Project/NWXCMake
)
FetchContent_MakeAvailable(nwx_cmake)
list(APPEND CMAKE_MODULE_PATH "${nwx_cmake_SOURCE_DIR}/cmake")

set(
    CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${PROJECT_SOURCE_DIR}/cmake"
    CACHE STRING "" FORCE
)

include(get_cmaize)
include(nwx_versions)

### Options ###
option(BUILD_TESTING "Should we build the tests?" OFF)
option(BUILD_PYBIND11_PYBINDINGS "Use Pybind11 to build Python bindings?" ON)
option(ENABLE_NWCHEM "Should we build supporf for friend: NWChem ?" ON)


## Find friends ##
include(nwchem)

## Configure file with enabled friends ##
set(friends_template "${CMAKE_CURRENT_LIST_DIR}/cmake/friends.py.in")
set(python_src_directory "${CMAKE_CURRENT_LIST_DIR}/src/python")
configure_file(
    "${friends_template}"                            # Input file
    "${python_src_directory}/friendzone/friends.py"  # Output file
    @ONLY                                            # Only replace @ variables
)

## Build FriendZone's dependencies ##
cpp_find_or_build_dependency(
    simde
    URL github.com/NWChemEx-Project/SimDE
    PRIVATE TRUE
    VERSION ${NWX_SIMDE_VERSION}
    BUILD_TARGET simde
    FIND_TARGET nwx::simde
    CMAKE_ARGS BUILD_TESTING=OFF
)

if("${NWX_MODULE_DIRECTORY}" STREQUAL "")
    message(
        FATAL_ERROR "NWX_MODULE_DIRECTORY must be set to the directory "
                    "where you would like the Python modules installed."
    )
endif()


if("${BUILD_TESTING}")
    include(CTest)
    include(nwx_pybind11)
    set(PYTHON_TEST_DIR "${CMAKE_CURRENT_LIST_DIR}/tests/python")

    message("calling nwx_pybind11_tests")
    nwx_pybind11_tests(
        pyFriendZone_unit_tests
        "${PYTHON_TEST_DIR}/unit_tests/test_friendzone.py"
        SUBMODULES simde chemist pluginplay parallelzone
    )
endif()

install(
    DIRECTORY "${python_src_directory}/friendzone"
    DESTINATION "${NWX_MODULE_DIRECTORY}"
)
