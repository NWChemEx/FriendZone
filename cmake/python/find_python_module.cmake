# Copyright 2023 NWChemEx-Project
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

include_guard()

#[[[ Attempts to find a Python module, returns whether it was found or not.
#
# This function will invoke the pip module through the Python interpreter and
# see if the specified module appears in the list of installed modules. The
# result of this inquiry is then returned
#
# :param was_found: Used to return the result
# :type was_found: *bool
# :param module_name: The name of the Python module to look for.
# :type module_name: str
#]]
function(find_python_module fpm_was_found fpm_module_name)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "-m" "pip" "list"
        COMMAND grep -w "${fpm_module_name}"
        OUTPUT_VARIABLE _fpm_modules
    )
    if("${_fpm_modules}" STREQUAL "")
        set("${fpm_was_found}" FALSE PARENT_SCOPE)
    else()
        set("${fpm_was_found}" TRUE PARENT_SCOPE)
    endif()
endfunction()

#[[[ Raises a fatal error if a Python module is not installed.
#
#  This function is a thin wrapper around ``find_python_module`` that asserts
#  that the return value of ``find_python_module`` is TRUE. If the value
#  returned from ``find_python_module`` is not TRUE this function will raise
#  a fatal error.
#
#  :param module_name: The name of the Python module which must be installed.
#  :type module_name: str
#]]
function(assert_python_module apm_module_name)
    find_python_module(_apm_was_found "${apm_module_name}")
    if(NOT "${_apm_was_found}")
        message(
            FATAL_ERROR
            "Unable to locate Python module: ${apm_module_name}"
        )
    endif()
endfunction()
