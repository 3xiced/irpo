# cpr

if(WIN32 AND (${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME}))
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_PATH}/$<CONFIG> CACHE INTERNAL "" FORCE)
endif()

set(CPR_COMPAT ON CACHE INTERNAL "" FORCE)
set(CPR_ENABLE_TESTS OFF CACHE INTERNAL "" FORCE)

FetchContent_Declare(
  cpr GIT_REPOSITORY https://github.com/libcpr/cpr.git
   GIT_TAG 3020c34ae2b732121f37433e61599c34535e68a8)
FetchContent_MakeAvailable(cpr)
include_directories(${cpr_SOURCE_DIR}/include)
install(
    TARGETS cpr 
    EXPORT cpr
    # More arguments as necessary...
  )
