#include "rclcpp/rclcpp.hpp"
#include <wiringPi.h>

class MotorNode: public rclcpp::Node
{
public:
	MotorNode() : Node("motor_node")
	{
		RCLCPP_INFO(this->get_logger(), "motor node initialized");
		
		if(wiringPiSetupGpio()==-1){
		RCLCPP_ERROR(this->get_logger(), "error initializing wiringpi");
		}
	}
	
private:
};

int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<MotorNode>();
	rclcpp::spin(node);
	rclcpp::shutdown();
	
	return 0;
}
