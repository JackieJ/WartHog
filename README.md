##FSM/Controller   
###Gist
The finites state machine controls and decides the next movement of the robot based on inputs. The input data       
should be already formatted in the expected way and the machine should do less data conversion as much as possible     
(i.e. position data like [lon, lat] in LL cannot be accepted since the expected format is [x,y] in UTM). All       
conversion should be taken care of by external nodes except conversion in kinematics for mathematical calculation    
(divide and conquer). The output of the machine decides the next move of the bot and is sent to the motor node.
Here is the FSM graph if you don't want to read through the code. Transitions happen when the conditions are met     
and data IO is processed within each state.
![FSM](https://raw.github.com/CloudClown/WartHog/jackie/Doc/FSM.png)
###Inputs      
* Target Coord from the waypoint Queue [x,y]+ (User Defined and Load before Execution);      
* GPS Fix: UTM ([x,y]);
* Camera: RegionOfInterest [x,y,width,height,flag]
* Bumper: True/False;
* Previous Motor Linear/Angular Speed Output: speed.linear, speed.angular
* Gyro: Headings (Here assumes the x-y pin's full range output is up to 360 degree);
* Kill Swtich: True/False;
* Diagnostic Message Aggregator: battery level, connectivity

###States (Priorities: Terminate > Obstacle > Target > Detector > Walk)
P.S.read the comments in the code, you don't need to understand the syntax. loose implementation, subject to change by tests.      
The controller we are implementing works as a simple [Mealy Machine](http://en.wikipedia.org/wiki/Mealy_machine)
#####Walk
Walk state is activated when the transition condition MODE == WALK
* Relevant Input: 
  * Target Coord
  * Current GPS Fix(UTM[x,y]). If you don't know about UTM, here is the 
    [wiki page](http://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system)
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
  if MODE == WALK:
  
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
  
  #transition to TARGET mode if the absolute distance from the 
  #target is shorter than 3 meters and the absolute
  #angle err is less than 10 degree (need calibaeration)
  if distanceFromTheTarget < 3 and math.fabs(angleErr) <= 10:
    MODE = DETECTOR
    break
  
  #Err correction based on the heading and distance errs
  #Objective: Try to keep the err within 10 degrees 
  #(within the same relative quadrant) (need caliberation)
    
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
* Relavent Input: 
 * Region of Interest: ROI(x,y,height,width, flag)
 * Current GPS Fix [x,y] in UTM
* Output: none (Detector transit to either the obstacle mode or the target mode)
* Loose implementation of the detector:

```python
 #monitor the ROI from the camera all the time
 while (1):
  flag = ROI.flag
  #distance from target is calculated using the GPS fix and target coordinate
  if (MODE != TARGET and distanceFromTarget < 3):
   MODE = TARGET
  elif (flag == Obstacle && MODE != OBSTACLE):
   MODE = OBSTACLE
  elif (MODE != WALK)
   MODE = WALK
```

#####Obstacle
Obstacle mode is activated when the transition condition MODE == OBSTACLE
* Relevant Input:
 * Region of Interest: ROI(x,y,height,width,flag)
 * Current GPS Fix [x,y] in UTM
 * Loose implementation of the obstacle state
* Output: nextSpeed

```python
 #Objective: Make the robot move so that it's away from the ROI where the obstacle is centered
 #so far we hard code it to back up, turn and continue (will make specific implementation
 #based on tests)
 if (ROI.flag == Obstacle):
   #back up for 2 seconds
   while (true):
    nextSpeed.linear = -LINEARMAXSPEED
    nextSpeed.linear = -ANGULARMAXSPEED
    publish(nextSpeed)
    sleep(2)
    break
 else:
  MODE = DETECTOR
```

#####Target
Target mode is activated when the transition condition MODE == TARGET
* Relevant Input:
 * Region of Interest: ROI(x,y,height,width,flag)
 * Current GPS Fix [x,y] in UTM
 * Loose implementation of the obstacle state
* Output: nextSpeed
* Loose Implementation

```python
 #Objective: Put the target within the threshhold and go forward until it touches the cone
 
 #if bumper is hit and the distance is smaller than 1(needs caliberation, stops back up and go to next target)
 #back to walk mode
 if (bumper and distanceFromTarget < 1):
  currentTargetCoord = targetCoordQueue.shift()
  #back up and turn
  nextSpeed.linear = -LINEARMAXSPEED
  nextSpeed.angular = -ANGULARMAXSPEED
  sleep(2)
  MODE = WALK
 
 #calculate the center of the ROI, based on the image frame size from the camera
 COR_X = ROI.x_offset + ROI.width / 2 - self.image_width / 2
 #move bot accordingly based the difference between COR and the threshhold
 #the target pos exceeds threshhold in x-direction, that's the only direction we care about
 if abs(COR_X) > XTHRESHHOLD
   if COR_X > 0
    nextSpeed.angular = 1
   else 
    nextSpeed.angular = -1
  nextSpeed.linear = 0
 else 
  nextSpeed.linear = 1
  nextSpeed.angular = 0
  
 publish(nextSpeed)
```

#####Terminate
Target mode is activated when the transition condition MODE == TERMINATE
* Relevant Input:
 * Bumper (True/False)
 * Kill Swtich (True/False)
 * Diagnostic Aggregator (Battery Level)
* Loose implementation

```python
 #Objective: Stop the bot or act accordingly
 if killSwitch or batteryLevel < THRESHHOLD:
  nextSpeed.linear = 0
  nextSpeed.linear = 0
  publish(nextSpeed)
 #if the bump is hit way before reaching the target. Hardcode it so that it back up
 #and turn
 if (Bumper and distanceFromTarget > 3):
  nextSpeed.linear = -LINEARMAXSPEED
  nextSpeed.angular = -ANGULARMAXSPeED
  publish(nextSpeed)
  sleep(2)
 
```
