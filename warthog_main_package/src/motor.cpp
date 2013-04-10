#include <stdlib.h>
#include <stdio.h>
#include <ros/ros.h>
#include <turtlesim/Velocity.h>
#include "AX3500.h"

AX3500 motor;

void setVelocity(const turtlesim::Velocity::ConstPtr& msg) {
  int linear = (int) (msg->linear*5);
  int angular = (int) (msg->angular*5);
  
  std::cout << linear << "\n";
  std::cout << angular << "\n";
  motor.SetSpeed(AX3500::CHANNEL_LINEAR, -angular);
  motor.SetSpeed(AX3500::CHANNEL_STEERING, -linear);
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "WarthogControl_node");

  
  motor.Open("/dev/ttyUSB0", true); // Enable safety cutoff
  std::cout << "Connecting to motor controller...\n";
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("motor_velocity", 1000, setVelocity);
  ros::spin();

  motor.Close();
  return 0;
}
