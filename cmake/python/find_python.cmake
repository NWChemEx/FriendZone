include_guard()

#[[[ Wraps the process of finding the Python interpreter.
#
# At the moment this is a thin wrapper around find_package with our preffered
# options.
#]]
function(find_python)
    find_package(Python3 COMPONENTS Interpreter QUIET REQUIRED)
    message(STATUS "Found Python3: ${Python3_EXECUTABLE}")
endfunction()

find_python()
