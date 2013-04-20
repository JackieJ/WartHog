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
        self.targetCoord = waypoints.pop(0)
        self.targetPose = self.targetCoord
        #Constants
        self.MAXLINEAR = 3
        self.MAXANGULAR = 3
        #############for tests#############
        self.testGain = -1
        #self.velocityOutput.linear = self.MAXLINEAR
        #self.velocityOutput.angular = 01
        #############for tests##############

    def run(self):
        while not rospy.is_shutdown():
            #subscribers
            self.killSwitchSub = rospy.Subscriber("kill", Bool, self.killSwitchCallback)
            self.bumperSub = rospy.Subscriber("bump", Bool, self.bumperCallback)
            self.gpsUTMSub = rospy.Subscriber("odom", Odometry, self.GPSUTMCallback)
            self.cvSub = rospy.Subscriber("cone", String, self.cvCallback)
            #gyro headings
            #self.gyroSub = rospy.Subscriber("gyro", Float32, self.headingCallback)
            time.sleep(1)
            
    def GPSUTMCallback(self, data):
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
        
    def cvCallback(self, data):
        if data.data == 'F':#too close
            rospy.loginfo("cv:filled")
            self.linearSpeed = 0
            self.angularSpeed = 0
        if data.data == 'R':#on the right
            rospy.loginfo("cv:on the right")
            self.linearSpeed = 1
            self.angularSpeed = -self.MAXANGULAR
        if data.data == 'L':#on the left
            rospy.loginfo("cv:on the left")
            self.linearSpeed = 1
            self.angularSpeed = self.MAXLINEAR
        if data.data == 'M':#in the center
            rospy.loginfo("cv:in the center")
            self.linearSpeed = 1
            self.angularSpeed = 0
        rospy.loginfo("publishing cv")
        self.publish()
        
    def headingCallback(self, data):
        #heading test
        print >> sys.stdout, "heading:", data.data
        #print >> sys.stdout, "float32", type(std_msgs.msg.Float32(0.0))
        if data.data > 0.0 and data.data <= 180.0:
            print >> sys.stdout, "turning left"
            self.velocityOutput.angular = 3
        elif data.data > 180.0 and data.data <= 359.0:
            print >> sys.stdout, "turning right"
            self.velocityOutput.angular = -3
        print >> sys.stdout, "publishing:", self.velocityOutput.angular    
        self.motorPublisher.publish(self.velocityOutput)

    def killSwitchHook(self):
        #extra guarantee for kill switch shutdown
        self.velocityOutput.linear = 0
        self.velocityOutput.angular = 0
        self.motorPublisher.publish(self.velocityOutput)

    def killSwitchCallback(self, data):
        #if kill switch is true shutoff the whole system
        if data.data:
            rospy.on_shutdown(self.killSwitchHook)
            self.isKilled = True
            self.publish()
            rospy.signal_shutdown("KILL SWITCH TRIGGERED! SYSTEM SHUTDOWN")
                        
    def bumperCallback(self, data):
        if data.data:
            #test
            self.velocityOutput.linear = -self.velocityOutput.linear
            #test
            #if bumper is true, pop out the target coord and go to the next
            
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
