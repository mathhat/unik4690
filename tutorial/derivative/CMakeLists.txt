cmake_minimum_required(VERSION 2.8)
project( bart )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( derivative derivative.cpp )

target_link_libraries( derivative ${OpenCV_LIBS} )

