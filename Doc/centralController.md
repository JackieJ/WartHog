##FSM/Controller      
###Inputs      
* Target Coord from the Coord Queue [x,y]+ (User Defined and Load before Execution);      
* GPS Fix: LL to UTM ([Lon, Lat] => [x,y]);
* Camera: 
* Bumper: True/False;
* Previous Motor Linear/Angular Speed Output: speed.linear, speed.angular
* Gyro: Headings (Here assumes the x-y pin's full range output is up to 360 degree);
* Kill Swtich: True/False;
* Diagnostic Message Aggregator: battery level, connectivity

###States (Priorities: Kill > Obstacle > Target > Detector > Walk)
#####Walk
* Relevant Input: 
  * Target Coord
  * Current GPS Fix(UTM[x,y])
  * Current Motor Speed(Linear, Angular)
  * Headings (0-360)
* Output: Speed

```python        
  #flow of the walk state 
  
  while walkStateIsEnabled:
  
  #difference calculation
  #the current GPS Fix is obtained from the GPS msg, which is published by GPS
  errX = coord[x] - currentGPSUTMFix[x] 
  errY = coord[y] - currentGPSUTMFix[y]
  
  distancePow = pow(errX, 2) + pow(errY, 2)
  distanceFromTheTarget = sqrt(distancePow)
  
```         

#####Detector

#####Obstacle

#####Target

#####Kill
