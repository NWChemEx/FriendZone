include_guard()

#[[[ Wraps the process of finding the Python interpreter.
#
# At the moment this is a thin wrapper around find_package with our preffered
# options.
#]]
function(find_python)
    find_package(Python3 COMPONENTS Interpreter QUIET REQUIRED)
    message(DEBUG "Found Python3: ${Python3_EXECUTABLE}")
endfunction()

function(assert_has_pip)
    execute_process(
        COMMAND "${Python3_EXECUTABLE}" "-m" "pip" "--version"
        COMMAND "cut" "-d " "-f4"
        OUTPUT_VARIABLE _ahp_hint
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()

find_python()
