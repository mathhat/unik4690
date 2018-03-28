cmake_minimum_required( VERSION 3.5.1 )

project(lab_0_intro)

set(CMAKE_CXX_STANDARD 11)

# Compiler flags
set(compiler_options -Wall -Wextra -Wpedantic)

# Find libraries
find_package(OpenCV 3.3.1 REQUIRED)
find_package(sophus REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} )
target_include_directories(${PROJECT_NAME} SYSTEM PRIVATE ${sophus_INCLUDE_DIRS})
target_compile_options(${PROJECT_NAME} PRIVATE ${compiler_options})
