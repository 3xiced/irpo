# Set the minimum version of CMake that can be used
# To find the cmake version run
# $ cmake --version
cmake_minimum_required(VERSION 3.5)

# Set the project name
project (sample)

add_executable(sample "main.cpp")
# set(onyx_DIR "../onyx-lm/build/")
target_link_libraries(sample PRIVATE onyx::onyx)