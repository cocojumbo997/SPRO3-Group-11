cmake_minimum_required(VERSION 3.8)
project(cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(node_template src/node_template.cpp)
ament_target_dependencies(node_template rclcpp)

add_executable(test_node src/test_node.cpp)
ament_target_dependencies(test_node rclcpp)
target_link_libraries(test_node wiringPi)

add_executable(LIDAR_node src/LIDAR_node.cpp)
ament_target_dependencies(LIDAR_node rclcpp)
target_link_libraries(LIDAR_node wiringPi)

add_executable(motor_node src/motor_node.cpp)
ament_target_dependencies(motor_node rclcpp)
target_link_libraries(motor_node wiringPi)

install(TARGETS
	node_template
	test_node
	LIDAR_node
	motor_node
	DESTINATION lib/${PROJECT_NAME}
)

ament_package()
