##FSM/Controller   
###Inputs      
* Target Coord from the waypoint Queue [x,y]+ (User Defined and Load before Execution);      
* GPS Fix: LL to UTM ([Lon, Lat] => [x,y]);
* Camera: 
* Bumper: True/False;
* Previous Motor Linear/Angular Speed Output: speed.linear, speed.angular
* Gyro: Headings (Here assumes the x-y pin's full range output is up to 360 degree);
* Kill Swtich: True/False;
* Diagnostic Message Aggregator: battery level, connectivity

###States (Priorities: Terminate > Obstacle > Target > Detector > Walk)
P.S.read the comments in the code, you don't need to understand the syntax. loose implementation, subject to change by tests.      
The controller we are implementing works as a simple [Mealy Machine](http://en.wikipedia.org/wiki/Mealy_machine)
#####Walk
* Relevant Input: 
  * Target Coord
  * Current GPS Fix(UTM[x,y]). If you don't know about UTM, here is the [wiki page](http://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system)
  * Current Motor Speed(Linear, Angular)
  * Headings (0-359, Gyro code needs to -360 to angles > 359 and +360 to angles < 0 until is's within the range      
    between 0 to 360
* Output: Speed
* Flow of the walk state

```python        
  #flow of the walk state
  
  #globals(to be defined based on tests)
  currentTargetCoord (x,y)
  LINEARSPEEDMAX #maximum linear speed allowed
  ANGULARSPEEDMAX #maximum angular speed allowed
  nextSpeedTwist (angular, linear) 
  #Speed Value Convention(subject to change): 
  #+linear:forward, -linear:backward, +angular:yaw clockwise, -angular:yaw counterclockwise
  
  #start if the transition hits the WALK state
  while MODE == WALK:
  ############
  #Kinematics#
  ############
  
  #the current GPS Fix is obtained from the GPS msg, which is published by GPS
  errX = currentTargetCoord[x] - currentGPSUTMFix[x] 
  errY = currentTargetCoord[y] - currentGPSUTMFix[y]
  
  #calculate the distance between the bot and the target. Pythagorean theorem
  distancePow = pow(errX, 2) + pow(errY, 2)
  distanceFromTheTarget = sqrt(distancePow)
  
  #angle compared against gyro data (simple trignometry calculation)
  targetAngle = math.atan2(err_y,err_x)*(180/math.pi) #convert radian to degree
  
  #Convert the targetAngle to a positive value based on the 0 reference
  while (targetAngle < 0) :
   targetAngle += 360
  
  angleErr = targetAngle - heading # the heading is obtained from the gyro
  
  #transition to DETECTOR mode if the absolute distance from the target is shorter than 3 meters and the absolute
  #angle err is less than 10 degree (need calibaeration)
  if distanceFromTheTarget < 3 and math.fabs(angleErr) <= 10:
    MODE = DETECTOR
    break
  
  #Err correction based on the heading and distance errs
  #Objective: Try to keep the err within 10 degrees (within the same relative quadrant) (need caliberation)
    
  #calculate the speed based on angleErr
  linear = 0
  angular = 0
  #case 1:90 <= angleErr <= 180 or angleErr <= -180
  if (angleErr >= 90 and angleErr <= 180) or (angleErr <= -180): 
   linear = 0
   angular = -ANGULARMAXSPEED
  elif (angleErr <= -90 and angleErr >= -180) or (angleErr > 180):
   #case 2: -180 <= angleErr <= -90 or angleErr > 180
   linear = 0
   angular = ANGULARMAXSPEED
  elif (angleErr > -90 && angleErr < 90) :
   #If the error range is -90 < angleErr < 90
   #the linear and angular speed is decided by trig functions of the angleErr and the maximum speeds
   linear = math.cos(angleErr)*LINEARMAXSPEED
   angular = math.sin(angleErr)*ANGULARMAXSPEED
  
  nextSpeedTwist.linear = linear
  nextSpeedTwist.angular = angular
  
  #publish the next twist message to the topic the motor listens to 
  publish(netxSpeedTwist);
```         

#####Detector
Detector mode is activated when the transition condition MODE == DETECTOR
#####Obstacle
Obstacle mode is activated when the transition condition MODE == OBSTACLE
#####Target
Target mode is activated when the transition condition MODE == TARGET
#####Terminate
Target mode is activated when the transition condition MODE == TERMINATE
