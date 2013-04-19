#!/usr/bin/python

#Author: Jackie Jin
#License: BSD

import rospy
from std_msgs.msg import *
import roslib; roslib.load_manifest('gps_common')
from gps_common.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import yaml
import sys
import time
import math

class ConeCoordsGetter():
    def __init__ (self):
        rospy.init_node('FSM')
        print >> sys.stdout, "creating the yaml file waypoings.yaml!"
        self.stream = file('/home/robo/Projects/WartHog/warthog_main_package/src/waypoints.yaml', 'w+')
        self.coordData = []
        
    def run(self):
        while not rospy.is_shutdown():
            #print >> sys.stdout, "waiting for input..."
            self.gpsUTMSub = rospy.Subscriber("odom", Odometry, self.GPSUTMCallback)
            time.sleep(2)
            
    def GPSUTMCallback(self, data):
        print >> sys.stdout, "pose_x:", data.pose.pose.position.x
        print >> sys.stdout, "pose_y:", data.pose.pose.position.y
        coord = {
            'x':0,
            'y':0,
            'hasCone': False,
            'direction':" " #back up left ("L"), back up right ("R")
            }
        coord['x'] = data.pose.pose.position.x
        coord['y'] = data.pose.pose.position.y
        self.coordData.append(coord)
        yaml.dump(self.coordData, self.stream)
             
if __name__ == '__main__':
    try:
        getter = ConeCoordsGetter()
        getter.run()
    except rospy.ROSInterruptException:
        pass
