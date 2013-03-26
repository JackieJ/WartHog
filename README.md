##TODO         
 * Design flows       
 * Milestones
 * determine what the zero point for the gyroscope should be (currently is 180 degrees)
 * double check gyro output matches the expected gyro input for the Walk code (central Controller)

##Wiring of IMU (5 Degrees of Freedom) to Arduino
IMU Board <--> Arduino  
x-axis/accx <--> Analog 0  
y-axis/accy <--> Analog 1  
z-axis/accz <--> Analog 2  
VRef <--> 3.3V  
y-rate/gyroY <--> Analog 5  
x-rate/gyroX <--> Analog 4  
GND <--> GND  
3.3V <--> 3.3V 

##Gyroscope
###Overview
* The gyro measures rotational movement in degrees per second.
* The IDG-300 gyroscope measures the rotational movement about the y-axis 
and the x-axis and outputs them as analog signals.
* When stationary, the gyroscope measurements should be zero.

######Input
* Analog readings (0 to 1023 values)

```c++
 double reading = analogRead(pin);
```
* gyro reading when the gyro is at "zero position" (horizontal/flat on the table)

```c++
 //find the "zero position" values experimentally by printing out the "zero position" values
 Serial.print(analogRead(xgyroPin));
 Serial.print(analogRead(ygyroPin));
```
```c++
const int gyroZeroX = 484;
const int gyroZeroY = 472;  
```

######Output
* Degrees/second

``` c++
 double getGyroRate(int pin)
{
 delay(1); //delay between readings for stability
 double reading = analogRead(pin); 
 
 //gyroY and gyroX have different "zero positions"
 if(pin == xgyroPin)
   return double((reading - gyroZeroX) / gyroScale); //in degrees/sec
 else
   return double((reading - gyroZeroY) / gyroScale); 
}
```

* Degrees/second to degrees
  * need to take the time between now and the last time the loop was run

```c++
  //time passed since last loop in seconds  
  //micros() gives you the time the program has been running in microseconds
  timeDiff = (micros() - lastLoopTime)/1000000;   
    
  double gyroXangle = getGyroRate(xgyroPin)*timeDiff;
  double gyroYangle = getGyroRate(ygyroPin)*timeDiff;
  
  //update the lastLoopTime
  lastLoopTime = micros();
```

##Accelerometer
###Overview
The accelerometer measures Earth's gravitational acceleration (g) in 3-D. 
Measurements  are initially as analog signals.

##Complimentary Filter
###Overview
* The gyro has a tendency to drift (the output from the gyro no longer accurately reflects the
rotational movement) as time increases and can become unreliable.
* The drift can be reduce by incoporating the accelerometer angles using a technique called Complimentary Filter.
* There is also the Kalman Filter that reduces the drift even more, but
the calculations are more complicated and the Complimentary Filter produces almost the same result.

###Calculation
compAngle = 0.93*(compAngle + gyroangle*changeInTime)+(0.07*accAngle);
