#!/usr/bin/python

#Author: Jackie Jin
#License: BSD

import rospy
from std_msgs.msg import String
import roslib; roslib.load_manifest('gps_common')
from gps_common.msg import *
from sensor_msgs.msg import *
from turtlesim.msg import *
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
        self.currentTwist = {
            'utm':{
                'x':.0,
                'y':.0
                },
            'angle':.0
            }
        self.targetTwist = {
            'utm':{
                'x':.0,
                'y':.0
                },
            'angle':.0
            }
        #load waypoints from the yaml file
        self.waypoints = yaml.load(file('/home/robo/Projects/WartHog/warthog_main_package/src/waypoints.yaml','r'))
       
    def run(self):
        pass

    def cvCallback(self, data):
        pass
    
    def headingCallback(self, data):
        pass
        
    def killSwitchCallback(self, data):
        pass
        
    def bumperCallback(self, data):
        pass

    def vCalc(self):
        pass
        
    def publisher(self):
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
