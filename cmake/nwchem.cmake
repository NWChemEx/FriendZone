include_guard()
include(python/python)

#[[[ Determines if NWChem and the necessary Python interface are installed.
#
#  At present FriendZone can not install
#]]
function(find_nwchem)
    find_program(NWCHEM_FOUND nwchem REQUIRED)
    assert_python_module("qcelemental")
    assert_python_module("qcengine")
    assert_python_module("networkx")
    message("Found nwchem: ${NWCHEM_FOUND}")
endfunction()

if("${ENABLE_NWCHEM}")
    find_nwchem()
endif()
