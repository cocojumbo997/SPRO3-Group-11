#include "rclcpp/rclcpp.hpp"
#include <wiringPi.h>

class LidarNode: public rclcpp::Node
{
public:
	
	LidarNode() : Node("Lidar_Node")
	{
		RCLCPP_INFO(this->get_logger(), "lidar node initialized");
		
		if(wiringPiSetupGpio()==-1){
		RCLCPP_ERROR(this->get_logger(), "error initializing wiringpi");
		}
	}
	
private:
};

int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<LidarNode>();
	rclcpp::spin(node);
	rclcpp::shutdown();
	
	return 0;
}
