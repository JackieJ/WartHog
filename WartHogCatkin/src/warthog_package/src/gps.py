#!/usr/bin/env python
#Author: Jackie Jin
#Des: interface with gpsd
import sys
import time
import rospy
from gps import *
import roslib; roslib.load_manifest('gps_common'); roslib.load_manifest('gps')
from gps_common.msg import *


class GPSD():
    def __init__(self):
        rospy.init_node('GPSD')
        self.fixPub = rospy.Publisher('gps/fix', GPSFix)
        self.session = gps()
        self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
        self.currentVal = None
        self.currentFix = GPSFix()

    def getCurrentVal(self):
        return self.currentVal

    def publish(self):
        try:
            self.currentFix.latitude = self.currentVal['lat']
            self.currentFix.longitutde = self.currentVal['lon']
        except Exception as err:
            print >> sys.stderr, err
        self.fixPub.publish(self.currentFix)

    def run(self):
        while not rospy.is_shutdown():
            try:
                while True:
                    self.currentVal = self.session.next()
                    self.publish()
            except stopIteration:
                print >> sys.stderr, "stop iteration!"

if __name__ == '__main__':
    gpsd = GPSD()
    try: 
        gpsd.run()
    except rospy.ROSInterrupException:
        pass
