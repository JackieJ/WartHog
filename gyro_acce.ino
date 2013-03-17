#include <ros.h>
#include <std_msgs/Empty.h>

ros::NodeHandle nh; 

#define RAD_TO_DEG  57296 / 1000
// these constants describe the pins. They won't change:
const int xpin = A0;                  // x-axis of the accelerometer
const int ypin = A1;                  // y-axis
const int zpin = A2;                  // z-axis (only on 3-axis models)
//const int 

int sampleDelay = 200;   //number of milliseconds between readings

void setup()
{
  nh.initNode();
  //nh.subscribe(sub);
  
  // initialize the serial communications:
  Serial.begin(9600);

  //Make sure the analog-to-digital converter takes its reference voltage from
  // the AREF pin
  analogReference(EXTERNAL);

  pinMode(xpin, INPUT);
  pinMode(ypin, INPUT);
  pinMode(zpin, INPUT);
}

int arctan2(int y, int x) {                                    // http://www.dspguru.com/comp.dsp/tricks/alg/fxdatan2.htm
   int coeff_1 = 128;                                          // angle in Quids (1024 Quids=360°)
   int coeff_2 = 3*coeff_1;
   float abs_y = abs(y)+1e-10;
   float r, angle;
   
   if (x >= 0) {
     r = (x - abs_y) / (x + abs_y);
     angle = coeff_1 - coeff_1 * r;
   }  else {
     r = (x + abs_y) / (abs_y - x);
     angle = coeff_2 - coeff_1 * r;
   }
   if (y < 0)      return int(-angle); 
   else            return int(angle);
}

void loop()
{
  int x = analogRead(xpin);

  //add a small delay between pin readings.  I read that you should
  //do this but haven't tested the importance
    delay(1); 

  int y = analogRead(ypin);

  //add a small delay between pin readings.  I read that you should
  //do this but haven't tested the importance
    delay(1); 

  int z = analogRead(zpin);

  //zero_G is the reading we expect from the sensor when it detects
  //no acceleration.  Subtract this value from the sensor reading to
  //get a shifted sensor reading.
  float zero_G = 512.0; 

  //scale is the number of units we expect the sensor reading to
  //change when the acceleration along an axis changes by 1G.
  //Divide the shifted sensor reading by scale to get acceleration in Gs.
  float scale = 102.3;

  //acceleration of each axis in g's
  float accX, accY, accZ;
  accX = (x - zero_G) / scale;
  accY = (y - zero_G) / scale;
  accZ = (z - zero_G) / scale;
  
//The sensors values vs position should read as follow:
//Horizontal  ( 0° =  0 Quid )   ACC_X: 0    ACC_Z: XX   GYR_X: 0
//Left side   (-90° = -256 Quid) ACC_X: XX   ACC_Z: 0    GYR_X: 0
//Right side (+90° = +256 Quid)  ACC_X:-XX   ACC_Z: 0    GYR_X: 0
//Reversed  (180° = +512 Quid)   ACC_X: 0    ACC_Z:-XX   GYR_X: 0
  
  
  double accXangle = (atan2(accX, accZ)+PI)*RAD_TO_DEG;
  double accYangle = (atan2(accY, accZ)+PI)*RAD_TO_DEG;
  
  
  Serial.print(accX);
  Serial.print("\t");

  Serial.print(accY);
  Serial.print("\t");

  Serial.print(accZ);
  Serial.print("\t");

  Serial.print(accXangle);
  Serial.print("\t");

  Serial.print(accYangle);
  Serial.print("\t");
  
  Serial.print("\n");

  // delay before next reading:
  delay(sampleDelay);
}
