#!/usr/bin/python

#Author: Jackie Jin
#License: BSD

import rospy
from std_msgs.msg import *
import roslib; roslib.load_manifest('gps_common')
from gps_common.msg import *
from sensor_msgs.msg import *
from turtlesim.msg import *
from nav_msgs.msg import *
import yaml
import sys
import time
import math

class FSM():
    def __init__ (self):
        rospy.init_node('FSM')
        rospy.loginfo("Initializing ROBOT.....")
        self.motorPublisher = rospy.Publisher('motor_velocity', Velocity)
        self.velocityOutput = Velocity()
        self.linearSpeed = 0
        self.angularSpeed = 0
        self.MODE = 0 #0 Walk; 1 Detector; 2 Target(bumper or Camera); 3 Kill
        self.isKilled = False
        self.currentPose = {
            'utm':{
                'x':.0,
                'y':.0
                },
            'heading':-99
            }
        #load waypoints from the yaml file
        #self.waypoints = yaml.load(file('/home/robo/Projects/WartHog/warthog_main_package/src/waypoints.yaml','r'))
        self.waypoints = yaml.load(open('/home/robo/Projects/WartHog/warthog_main_package/src/waypoints.yaml', 'r'))
        #retrieve target coordinates from the beginning of the list
        self.targetPose = self.waypoints.pop(0)
        #Constants. TWEAKING NEEDED
        self.MAXLINEAR = 3
        self.MAXANGULAR = 3
        #for generic walking vel
        self.linearGain = 0.2
        self.angularGain = 0.2
        #for full turning in walking mode
        self.fullTurnAngularGain = 0.2
        #for vel in camera mode
        self.cvLinearGain = 0.2
        self.cvAngularGain = 0.2
        #for vel when backing up
        self.backLinearGain = 0.2
        self.backAngularGain = 0.2
        #distance bound before entering the camera mode
        self.targetReachDistanceBound = 3
        #angle err bound before entering the camera mode
        self.angleErrBound = 10
        #############for tests#############
        self.testGain = -1
        #self.velocityOutput.linear = self.MAXLINEAR
        #self.velocityOutput.angular = 01
        #############for tests##############

    def run(self):
        while not rospy.is_shutdown():
            rospy.loginfo("Starting running process!")
            #subscribers
            self.killSwitchSub = rospy.Subscriber("kill", Bool, self.killSwitchCallback)
            self.bumperSub = rospy.Subscriber("bump", Bool, self.bumperCallback)
            self.gpsUTMSub = rospy.Subscriber("odom", Odometry, self.GPSUTMCallback)
            self.cvSub = rospy.Subscriber("cone", String, self.cvCallback)
            #gyro headings
            #self.gyroSub = rospy.Subscriber("gyro", Float32, self.headingCallback)
            time.sleep(1)

    def logging(msg):
        rospy.loginfo(msg)

    def GPSUTMCallback(self, data):
        #the walking mode has the lowest priority
        rospy.loginfo("GPS:if walking state....")
        if self.MODE == 0:
            rospy.loginfo("GPS: retrieving GPS data")
            #retrieve gps data first, then grab the gyro data
            (self.currentPose['utm'])['x'] = data.pose.pose.position.x
            (self.currentPose['utm'])['y'] = data.pose.pose.position.y
        
            #loggings
            print >> sys.stdout, "target_x", self.targetPose['x']
            print >> sys.stdout, "target_y", self.targetPose['y']
            if self.targetPose['hasCone']:
                print >> sys.stdout, "target has cone: yes"
            else:
                print >> sys.stdout, "target has cone: no"
                print >> sys.stdout, "target direction", self.targetPose['direction']
                print >> sys.stdout, "current pose_x:", self.currentPose['utm']['x']
                print >> sys.stdout, "current pose_y:", self.currentPose['utm']['y']
    
            #gyro heading
            self.gyroSub = rospy.Subscriber("gyro", Float32, self.headingCallback)
        rospy.loginfo("GPS: not in walking state......")
                
    def cvCallback(self, data):
        self.logging("got camera data!")
        if data.data == 'F':#too close
            self.MODE = 1
            rospy.loginfo("cv:filled")
            #target and backup
            self.backup(self.targetPose['direction'])
            time.sleep(3)
            self.targetPose = self.waypoints.pop(0)
            #back to walk mode
            self.MODE = 0
        if data.data == 'R':#on the right
            self.MODE = 1
            rospy.loginfo("cv:on the right")
            self.linearSpeed = self.MAXLINEAR * self.cvLinearGain
            self.angularSpeed = -self.MAXANGULAR * self.cvAngularGain
        if data.data == 'L':#on the left
            self.MODE = 1
            rospy.loginfo("cv:on the left")
            self.linearSpeed = self.MAXLINEAR * self.cvLinearGain
            self.angularSpeed = self.MAXLINEAR * self.cvAngularGain
        if data.data == 'M':#in the center
            self.MODE = 1
            rospy.loginfo("cv:in the center")
            self.linearSpeed = self.MAXLINEAR * self.cvLinearGain
            self.angularSpeed = 0
        if data.data == 'N':
            self.MODE = 1
            self.logging("CAMERA, looking for cone")
            self.linearSpeed = 0
            self.angularSpeed = self.MAXANGULAR * self.cvAngularGain
            
        rospy.loginfo("publishing cv")
        self.logging("CAMERA: Publishing....")
        self.publish()
        
    def headingCallback(self, data):
        # #heading test
        # print >> sys.stdout, "heading:", data.data
        # #print >> sys.stdout, "float32", type(std_msgs.msg.Float32(0.0))
        # if data.data > 0.0 and data.data <= 180.0:
        #     print >> sys.stdout, "turning left"
        #     self.velocityOutput.angular = 3
        # elif data.data > 180.0 and data.data <= 359.0:
        #     print >> sys.stdout, "turning right"
        #     self.velocityOutput.angular = -3
        # print >> sys.stdout, "publishing:", self.velocityOutput.angular    
        # self.motorPublisher.publish(self.velocityOutput)
        
        # retrieve the heading value from gyro and perform calculation
        self.logging("GYRO: retrieving heading data....")
        self.currentPose['heading'] = data.data
        #calculate the velocity based on target 
        self.vCalc()
        
        
    def killSwitchHook(self):
        #extra guarantee for kill switch shutdown
        self.velocityOutput.linear = 0
        self.velocityOutput.angular = 0
        self.motorPublisher.publish(self.velocityOutput)

    def killSwitchCallback(self, data):
        #if kill switch is true shutoff the whole system
        
        if data.data:
            self.logging("KILL: Kill switch triggered, shuting down!")
            rospy.on_shutdown(self.killSwitchHook)
            self.isKilled = True
            self.publish()
            rospy.signal_shutdown("KILL SWITCH TRIGGERED! SYSTEM SHUTDOWN")
                        
    def bumperCallback(self, data):
        if data.data:
            self.logging("bumper: bumpered pressed entering mode two")
            self.MODE = 2
            errX = self.targetPose['x'] - self.currentPose['utm']['x']
            errY = self.targetPose['y'] - self.currentPose['utm']['y']
            distancePow = math.pow(errX, 2) + math.pow(errY, 2)
            distanceFromTheTarget = math.sqrt(distancePow)
            if distanceFromTheTarget < 1:
                self.logging("bumper: within target range, poping out target and enter next target state")
                self.linearSpeed = 0
                self.angularSpeed = 0
                rospy.loginfo("Cone Reached Backing up")
                self.publish()
                time.sleep(2)
                self.backup(self.targetPose['direction'])
                time.sleep(3)
                #pop out the target and go to next target
                self.targetPose = self.waypoints.pop(0)
                self.logging("bumper: back to walk mode")
                self.MODE = 0

    def backup (self, direction):
        #backup left
        if direction == "L":
            self.logging("backing up left")
            self.linearSpeed = -self.MAXLINEAR * self.backLinearGain
            self.angularSpeed = -self.MAXANGULAR * self.backAngularGain
        elif direction == "R":
            self.logging("backing up right")
            self.linearSpeed = -self.MAXLINEAR * self.backLinearGain
            self.angularSpeed = self.MAXANGULAR * self.backAngularGain
        if direction != ' ':
            self.publish()
            
    def vCalc(self):
        #get err between the current position and the target coordinate
        errX = self.targetPose['x'] - self.currentPose['utm']['x']
        errY = self.targetPose['y'] - self.currentPose['utm']['y']
        
        #calculate distance between current and target
        distancePow = math.pow(errX, 2) + math.pow(errY, 2)
        distanceFromTheTarget = math.sqrt(distancePow)
        
        #angle between current and target
        targetAngle = math.atan2(errY, errX)*(180/math.pi)
        
        while targetAngle < 0:
            targetAngle += 360
        angleErr = targetAngle - self.currentPose['heading']
        
        if (angleErr >= 90 and angleErr <= 180) or angleErr <= -180:
            self.logging("vCalc: full turning....")
            self.linearSpeed = 0
            self.angularSpeed = -self.fullTurnAngularGain * self.MAXANGULAR
        elif angleErr > -90 and angleErr < 90:
            self.logging("vCalc: normal walking.....")
            self.linearSpeed = math.cos(angleErr) * self.MAXLINEAR * self.linearGain
            self.angularSpeed = math.sin(angleErr)* self.MAXANGULAR
            
        self.publish()
        
        if distanceFromTheTarget < self.targetReachDistanceBound and math.fabs(angleErr) <= self.angleErrBound: 
            #go to detection mode
            if self.targetPose['hasCone']:
                self.logging("go to the camera mode for detection")
                self.MODE = 1
            else:
                self.logging("go to the next target point")
                #goto next waypoint
                self.targetPose = self.waypoints.pop(0)
        
    def publish(self):
        if self.isKilled:
            self.velocityOutput.linear = 0
            self.velocityOutput.angular = 0
        else:
            try:
                self.velocityOutput.linear = self.linearSpeed
                self.velocityOutput.angular = self.angularSpeed
            except Exception as err:
                print >> sys.stderr, "failed to grab linear and angular speed!"
                self.velocityOutput.linear = 0
                self.velocityOutput.angular = 0
        self.logging("publisher: publishing vel message....")
        self.motorPublisher.publish(self.velocityOutput)
        

if __name__ == '__main__':
    try:
        fsm = FSM()
        fsm.run()
    except rospy.ROSInterruptException:
        pass
