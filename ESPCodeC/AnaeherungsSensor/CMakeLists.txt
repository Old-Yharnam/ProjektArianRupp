# The following five lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(AnaeherungsSensor)

add_custom_target(idf_fullclean
	COMMAND idf.py fullclean
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
	COMMENT "Running idf.py fullclean"
)

add_custom_target(idf_build
	COMMAND idf.py build
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
	COMMENT "Running idf.py build"
)

add_custom_target(idf_flash
	COMMAND idf.py flash
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
	COMMENT "Running idf.py flash"
)

add_custom_target(idf_clean_build_flash
	COMMAND idf.py fullclean
	COMMAND idf.py build
	COMMAND idf.py flash
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
	COMMENT "Running idf.py fullclean, build, and flash"
)
