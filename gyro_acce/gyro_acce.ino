#include <Wire.h>
#include <math.h>
#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh; 
std_msgs::Float32 gyro_msg;
ros::Publisher p("gyro", &gyro_msg);


#define RAD_TO_DEG  57296 / 1000
// these constants describe the pins. They won't change:
const int xaccPin = A0;           // x-axis of the accelerometer
const int yaccPin = A1;           // y-axis
const int zaccPin = A2;           // z-axis 
const int xgyroPin = A4;
const int ygyroPin = A5;

double lastLoopTime, timeDiff;

  //zero_G is the reading we expect from the sensor when it detects
  //no acceleration.  Subtract this value from the sensor reading to
  //get a shifted sensor reading.
const float zero_G_y = 508.0; 
const float zero_G_x = 508.5;
const float zero_G_z = 604.5;

  //scale is the number of units we expect the sensor reading to
  //change when the acceleration along an axis changes by 1G.
  //Divide the shifted sensor reading by scale to get acceleration in Gs.
const float accScale = 102.3;

// Scaling from analog in values to degree/s
// Sensitivity of the gyro: 2.0 mV/degree/s (.002mV/degres/s)
//    10 bits (1024 values) for 3.3 V: 3.22265625 mV per step
//    or: 1.611328125 degree/sec for each step
// (1024 values/3.3V) / (.002mV/degree/s)   = 1.611 degrees/sec
const float gyroScale = 1.612903226;

//AnalogIn values for zero change (x and y) for the gyro
//determined by looking at the analog value when the board was flat on table
//    Serial.print(analogRead(xgyroPin));
//    Serial.print(analogRead(ygyroPin));
int gyroZeroX = 0;
int gyroZeroY = 0;

int sampleDelay = 200;   //number of milliseconds between readings

double compAngleX = 0; // Calculate the angle using a Comlimentary Filter
double compAngleY = 0;

float curX = 0;
double curY = 0;

void setup()
{
  nh.initNode();
  nh.advertise(p);
  gyro_msg.data = 0;
  
  // initialize the serial communications:
  Serial.begin(57600);

  //Make sure the analog-to-digital converter takes 
  //its reference voltage from the AREF pin
  analogReference(EXTERNAL);

  pinMode(xaccPin, INPUT);
  pinMode(yaccPin, INPUT);
  pinMode(zaccPin, INPUT);
  pinMode(xgyroPin, INPUT);
  pinMode(ygyroPin, INPUT);
  
  for(int i=0; i<10; i++)
  {
    gyroZeroX += analogRead(xgyroPin);
    gyroZeroY += analogRead(ygyroPin);
  }
  gyroZeroX /= 10;
    gyroZeroY /= 10;
  
}

float getAccInG(int pin)
{
 delay(1);
 int count = 5;
 float reading = analogRead(pin);
 for(int i=0; i<count-1; i++)
 {
   reading+=analogRead(pin);
 }
 reading = reading/count;
 
 if(pin == xaccPin)
   return (reading - zero_G_x) / accScale;
 else if(pin == yaccPin)
   return (reading - zero_G_y) / accScale;
 else
   return (reading - zero_G_z) / accScale;
}

double getGyroRate(int pin)
{
  int count = 5;
double reading = analogRead(pin);

 for(int i=0; i<count-1; i++)
 {
   reading+=analogRead(pin);
 }
 reading = reading/count; 
 
 if(pin == xgyroPin)
 {
   reading = (reading - gyroZeroX) / gyroScale; //in degrees/sec
  if(reading <= 0.25 && reading >= -0.25)
     reading = 0;
   return reading;
 }
 else
   return (reading - gyroZeroY) / gyroScale; 
}

void loop()
{
  //acceleration of each axis in g's
  float accX, accY, accZ;
//  accX = getAccInG(xaccPin);
//  accY = getAccInG(yaccPin);
  //accZ = getAccInG(zaccPin);
  
  //flat on the table: accXangle and accYangle are 180 degrees
  //output should be 0 to 360 degrees
  //need to think about what angle should be starting position
//  double accXangle = ((atan2(accX, accZ)+PI)*RAD_TO_DEG);
//  double accYangle = (atan2(accY, accZ)+PI)*RAD_TO_DEG;
   
  //=================
  //gyro code
  
  //time passed since last loop in seconds  
  timeDiff = (micros() - lastLoopTime)/1000000;   
    
  double gyroXangle = getGyroRate(xgyroPin)*timeDiff;
  if(gyroXangle < .26 && gyroXangle > -.26)
    gyroXangle = 0;
 // double gyroYangle = getGyroRate(ygyroPin)*timeDiff;

/*  
  // Calculate the angle using a Complimentary filter
if(gyroXangle != 0)
  compAngleX = 0.93*(compAngleX+gyroXangle)+(0.07*accXangle); 
if(gyroYangle != 0)
  compAngleY = 0.93*(compAngleY+gyroYangle)+(0.07*accYangle); 


  Serial.print("compAngleX: ");
  Serial.print(compAngleX);Serial.print("\t");
    Serial.print("compAngleY: ");
  Serial.print(compAngleY); Serial.print("\t");
*/
//    Serial.print("gyroXangle: ");
//  Serial.print(gyroXangle); Serial.print("\t");
//  Serial.print("gyroYangle: ");
//  Serial.print(gyroYangle);  Serial.print("\t");

 
  curX += (gyroXangle)*3;   
  if(curX < 0)
    curX += 360;
    if(curX > 360)
    curX -= 360;
  
  
//  Serial.print("Cur x: ");
//  Serial.print(curX); Serial.print("\t");
//  Serial.print("\n");
  gyro_msg.data = curX;
   p.publish(&gyro_msg);

  lastLoopTime = micros();

  // delay before next reading:
  delay(sampleDelay);
     nh.spinOnce();
}
