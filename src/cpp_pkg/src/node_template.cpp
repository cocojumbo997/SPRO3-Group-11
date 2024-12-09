#include "rclcpp/rclcpp.hpp"

class NodeTemplate: public rclcpp::Node
{
public:
	NodeTemplate() : Node("node_name")
	{
	
	}
	
private:
};

int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<NodeTemplate>();
	rclcpp::spin(node);
	rclcpp::shutdown();
	
	return 0;
}
