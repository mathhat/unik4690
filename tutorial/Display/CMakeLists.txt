cmake_minimum_required(VERSION 2.8)
project( bart )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( display_image bart.cpp )
add_executable( blend_images blend.cpp )
target_link_libraries( display_image ${OpenCV_LIBS} )
target_link_libraries( blend_images ${OpenCV_LIBS} )

