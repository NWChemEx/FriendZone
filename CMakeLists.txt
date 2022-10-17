cmake_minimum_required(VERSION 3.14)
project(friendzone VERSION "1.0" LANGUAGES CXX)

set(
    CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${PROJECT_SOURCE_DIR}/cmake"
    CACHE STRING "" FORCE
)

include(get_cpp)

### Options ###
option(BUILD_TESTING "Should we build the tests?" OFF)

cpp_find_or_build_dependency(
    simde
    URL github.com/NWChemEx-Project/SimDE
    PRIVATE TRUE
    BUILD_TARGET simde
    FIND_TARGET nwx::simde
    CMAKE_ARGS BUILD_TESTING=OFF
)

if("${BUILD_TESTING}")
    include(CTest)
    cpp_find_or_build_dependency(
            mokup
            URL github.com/NWChemEx-Project/mokup
            PRIVATE
            BUILD_TARGET mokup
            FIND_TARGET nwx::mokup
            CMAKE_ARGS BUILD_TESTING=OFF
    )
    find_package(Python3 REQUIRED COMPONENTS Interpreter)
    add_test(
        NAME pyscf_api
        COMMAND ${Python3_EXECUTABLE} "-m" "unittest"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/tests/test_friendzone"
    )
    set_property(
        TEST pyscf_api
        PROPERTY ENVIRONMENT
            "PYTHONPATH=${PROJECT_SOURCE_DIR}/src:${CMAKE_BINARY_DIR}/Python"
    )
endif()
