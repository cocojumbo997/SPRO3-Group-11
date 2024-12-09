#include "rclcpp/rclcpp.hpp"
#include <wiringPi.h>

class TestNode: public rclcpp::Node
{
public:
	
	TestNode() : Node("node_name")
	{
		RCLCPP_INFO(this->get_logger(), "test node initialized");

		if(wiringPiSetupGpio()==-1){
		RCLCPP_ERROR(this->get_logger(), "error initializing wiringpi");
		}
		
		pinMode(23, INPUT);
		pullUpDnControl(23, PUD_DOWN);
		pinMode(24, OUTPUT);
		timer_ = this->create_wall_timer(std::chrono::milliseconds(500), 
										std::bind(&TestNode::timerCallback, this));
	}
	
private:
	
	int counter=0;
	void timerCallback()
	{
		if(counter%2==0){
		digitalWrite(24, HIGH);
		RCLCPP_INFO(this->get_logger(), "pin on");
		}
		else{
		digitalWrite(24, LOW);
		RCLCPP_INFO(this->get_logger(), "pin off");
		}
		counter++;
	}
	
	void gpioReading(){
		int value = digitalRead(23);
		if(HIGH==value){
		RCLCPP_INFO(this->get_logger(), "signal detected");
		}
	}
	rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<TestNode>();
	rclcpp::spin(node);
	rclcpp::shutdown();
	
	return 0;
}
