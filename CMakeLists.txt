cmake_minimum_required(VERSION "3.24.0")
set (CMAKE_CXX_STANDARD 17)

#Set target ouput directory
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

set(VALID_BUILD_TYPES "Release" "Debug" "MinSizeRel" "RelWithDebInfo")

option(BUILD_SHARED_LIBS "True when building a shared library" True)

project("onyx")

#set CMAKE_BUILD_TYPE default value
if(NOT CMAKE_CONFIGURATION_TYPES)
    if("${CMAKE_BUILD_TYPE}" STREQUAL "")
        set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build configuration" FORCE)
    endif()
endif()

#validate CMAKE_BUILD_TYPE
if(NOT CMAKE_CONFIGURATION_TYPES)
    list(FIND VALID_BUILD_TYPES "${CMAKE_BUILD_TYPE}" INDEX)
    if(${INDEX} MATCHES -1)
        message(FATAL_ERROR "Invalid build type. Valid types are [${VALID_BUILD_TYPES}]")
    endif()
endif()

#Create dropdown list for CMake gui
if(NOT CMAKE_CONFIGURATION_TYPES)
    if(DEFINED CMAKE_BUILD_TYPE)
        set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS ${VALID_BUILD_TYPES})
    endif()
endif()

include(FetchContent)
include(cmake/cpr_external.cmake)

add_subdirectory("onyx-lm")
add_subdirectory("sample")