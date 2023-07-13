include_guard()
include(python/find_python)

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
    assert_has_pip()
    execute_process(
        COMMAND "${Python3_EXECUTABLE}" "-m" "pip" "list"
        COMMAND grep "${fpm_module_name}"
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
