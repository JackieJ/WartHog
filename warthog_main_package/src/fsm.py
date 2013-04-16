#!/usr/bin/python

import rospy
from std_msgs.msg import String
import roslib; roslib.load_manifest('gps_common')
from gps_common.msg import *
from sensor_msgs.msg import *
from turtlesim.msg import *
import yaml
import sys
import time

class FSM():
    def __init__ (self):
        rospy.init_node('FSM')
        self.motorPublisher = rospy.Publisher('motor_velocity', Velocity)
        self.velocityOutput = Velocity()
        self.linearSpeed = 0
        self.angularSpeed = 0
        #load waypoints from the yaml file
        try:
            yamlStream = open("./waypoints.yaml", "r");
            self.waypoints = yaml.load(yamlStream)
        except IOError:
            print >> sys.stderr, "please run collectWaypoints.py before the launching!"
        
        
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
    except rospy.ROSInterruptException:
        pass
