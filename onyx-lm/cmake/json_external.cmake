# json

if(WIN32 AND (${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME}))
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_PATH}/$<CONFIG> CACHE INTERNAL "" FORCE)
endif()

set(JSON_COMPAT ON CACHE INTERNAL "" FORCE)
set(JSON_ENABLE_TESTS OFF CACHE INTERNAL "" FORCE)


FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)
include_directories(${json_SOURCE_DIR}/include)
install(
    TARGETS nlohmann_json 
    EXPORT nlohmann_json
    # More arguments as necessary...
  )
