add_library("${PROJECT_NAME}" "")
add_library(onyx::onyx ALIAS "${PROJECT_NAME}")

set(ONYX_EXPORT_FILE "Onyx-Exports")
install(TARGETS "${PROJECT_NAME}" EXPORT "${ONYX_EXPORT_FILE}")

target_include_directories("${PROJECT_NAME}" PUBLIC
	"$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
	"$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>" #foo_export.h
	"$<INSTALL_INTERFACE:include>" #${CMAKE_INSTALL_PREFIX}/include
)

if(NOT BUILD_SHARED_LIBS)
	set(STATIC_POSTFIX "-s")
	set_target_properties("${PROJECT_NAME}" PROPERTIES 
	COMPILE_FLAGS -DONYX_STATIC_DEFINE)
endif()

#Rename target Onyx
set_target_properties("${PROJECT_NAME}" PROPERTIES
	DEBUG_POSTFIX "${STATIC_POSTFIX}-d" 
	RELEASE_POSTFIX "${STATIC_POSTFIX}"
	MINSIZEREL_POSTFIX "${STATIC_POSTFIX}-mr"
	RELWITHDEBINFO_POSTFIX "${STATIC_POSTFIX}-rd"
)

include("GenerateExportHeader")
generate_export_header("${PROJECT_NAME}")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/onyx_export.h" DESTINATION "include")

# include cpr lib
target_link_libraries(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:cpr::cpr>")
target_link_libraries(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:nlohmann_json::nlohmann_json>")

add_subdirectory("include")
add_subdirectory("src")

set(ONYX_CONFIG_DIR "lib/cmake/${PROJECT_NAME}")
configure_file("${onyx_SOURCE_DIR}/cmake/OnyxConfig.cmake.in" "${onyx_BINARY_DIR}/${ONYX_CONFIG_DIR}/OnyxConfig.cmake")
install(FILES "${onyx_BINARY_DIR}/${ONYX_CONFIG_DIR}/OnyxConfig.cmake" DESTINATION "${ONYX_CONFIG_DIR}")
install(EXPORT "${ONYX_EXPORT_FILE}" DESTINATION "${ONYX_CONFIG_DIR}" NAMESPACE "onyx::")