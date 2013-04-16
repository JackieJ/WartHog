//kill switch
//press once, true
//press again, false
//press again, true
//etc

//bumpers
//press button, true
//release button, false

//referred to this tutorial: 
//http://ros.org/wiki/rosserial_arduino/Tutorials/Push%20Button

#include <ros.h>
#include <std_msgs/Bool.h>

ros::NodeHandle nh;

std_msgs::Bool kill_msg;
std_msgs::Bool bump_msg;
ros::Publisher pub_kill("kill", &kill_msg);
ros::Publisher pub_bump("bump", &bump_msg);

const int bump_pin = 7;
const int kill_pin = 6;

long debounce_delay=50;

bool bump_last_reading;
long bump_last_debounce_time=0;
bool bump_published = true;

bool kill_last_reading;
long kill_last_debounce_time=0;
bool kill_published = true;

void setup()
{
  nh.initNode();
  nh.advertise(pub_kill);
  nh.advertise(pub_bump);
  
  //initialize input pins for our buttons
  pinMode(kill_pin, INPUT);
  pinMode(bump_pin, INPUT);
  
  //Enable the pullup resistor on the button
  digitalWrite(kill_pin, HIGH);
  digitalWrite(bump_pin, HIGH);
  
  //The button is a normally button
  kill_last_reading = ! digitalRead(kill_pin);
  bump_last_reading = ! digitalRead(bump_pin);
}

bool status = false;

void kill_switch()
{
  bool kill_reading = !digitalRead(kill_pin);
  
  if (kill_last_reading!= kill_reading){
      kill_last_debounce_time = millis();
      kill_published = false;
      status = !status;
  }
  
  //if the button value has not changed during the debounce delay
  // we know it is stable
  if ( !kill_published && (millis() - kill_last_debounce_time)  > debounce_delay) 
  {
     if(kill_reading == true)
     {
      kill_msg.data = status;      
      pub_kill.publish(&kill_msg);
      kill_published = true;
      status = !status;
     }
  }
  kill_last_reading = kill_reading;
}

void bumper()
{
  bool bump_reading = !digitalRead(bump_pin);
  
  if (bump_last_reading!= bump_reading){
      bump_last_debounce_time = millis();
      bump_published = false;
  }
  
  //if the button value has not changed during the debounce delay
  // we know it is stable
  if ( !bump_published && (millis() - bump_last_debounce_time)  > debounce_delay) 
  {
      bump_msg.data = bump_reading;      
      pub_bump.publish(&bump_msg);
      bump_published = true;
  }
  bump_last_reading = bump_reading;
}

void loop()
{
  kill_switch();
  bumper();
  
  nh.spinOnce();
}

