set(FILES "${CMAKE_CURRENT_SOURCE_DIR}/onyx.cpp"
"${CMAKE_CURRENT_SOURCE_DIR}/SMBIOS.h"
"${CMAKE_CURRENT_SOURCE_DIR}/SMBIOS.cpp")
set(SUBDIRECTORIES "")
set(RELATIVE_PATH "src")

#Add all subdirectories 
foreach(VAR ${SUBDIRECTORIES})
	add_subdirectory(${VAR})
endforeach()

if(FILES)
	#Add source files to target
	target_sources("${PROJECT_NAME}" PRIVATE ${FILES})
	
	#Install our source files
	install(FILES ${FILES} DESTINATION ${RELATIVE_PATH})
endif()