##TODO         
 * Design flows       
 * Milestones

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
