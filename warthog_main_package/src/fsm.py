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
        self.motorPublisher = rospy.Publisher('motor_velocity', Velocity)
        self.velocityOutput = Velocity()
        self.linearSpeed = 0
        self.angularSpeed = 0
        self.MODE = 0 #0 Walk; 1 Detector; 2 Target(bumper); 3 Kill
        self.isKilled = False
        self.currentPose = {
            'utm':{
                'x':.0,
                'y':.0
                },
            'heading':-99
            }
        self.targetPose = {
            'utm':{
                'x':.0,
                'y':.0
                },
            'heading':-99
            }
        #load waypoints from the yaml file
        self.waypoints = yaml.load(file('/home/robo/Projects/WartHog/warthog_main_package/src/waypoints.yaml','r'))
        #Constants
        self.MAXLINEAR = 3
        self.MAXANGULAR = 1
        #############for tests#############
        self.testGain = -1
        self.velocityOutput.linear = self.MAXLINEAR
        self.velocityOutput.angular = 0
        #############for tests##############

    def test(self):
         self.motorPublisher.publish(self.velocityOutput);
        
    def run(self):
        
        while not rospy.is_shutdown():
            self.test()
            #subscribers
            self.killSwitchSub = rospy.Subscriber("kill", Bool, self.killSwitchCallback)
            self.bumperSub = rospy.Subscriber("bump", Bool, self.bumperCallback)
            self.gpsUTMSub = rospy.Subscriber("odom", Odometry, self.GPSUTMCallback)
                        
    def GPSUTMCallback(self, data):
        #retrieve gps data first, then grab the gyro data
        #gyro heading
        self.gyroSub = rospy.Subscriber("gyro", Float32, self.headingCallback)
            
    def cvCallback(self, data):
        pass
    
    def headingCallback(self, data):
        pass
        
    def killSwitchHook(self):
        #extra guarantee for kill switch shutdown
        self.velocityOutput.linear = 0
        self.velocityOutput.angular = 0
        self.motorPublisher.publish(self.velocityOutput)

    def killSwitchCallback(self, data):
        #if kill switch is true shutoff the whole system
        if data:
            rospy.on_shutdown(self.killSwitchHook)
            self.isKilled = True
            self.publish()
            rospy.signal_shutdown("KILL SWITCH TRIGGERED! SYSTEM SHUTDOWN")
                        
    def bumperCallback(self, data):
        if data:
            #test
            self.velocityOutput.linear = -self.velocityOutput.linear
            #test

    def vCalc(self):
        pass
        
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
        self.motorPublisher.publish(self.velocityOutput)
        

if __name__ == '__main__':
    try:
        fsm = FSM()
        fsm.run()
    except rospy.ROSInterruptException:
        pass
