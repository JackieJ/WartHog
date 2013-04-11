#!/usr/bin/python

import time
import sys
import serial
import string
import math
import calendar
from gps import *

import roslib
roslib.load_manifest('gps_common')
roslib.load_manifest('sensor_msgs')
import rospy
from  gps_common.msg import *
from sensor_msgs.msg import *



class GPSD():
	def __init__(self):
		rospy.init_node('GPSD')
                self.session = gps()
		self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
		self.currentVal = None
		self.fixPublisherLL = rospy.Publisher('fixLL', GPSFix)
                self.fixPublisherUTM = rospy.Publisher('fix', NavSatFix)
                self.currentFixLL = GPSFix()
                self.currentFixForUTM = NavSatFix()
                
        def get_currentVal(self):
		return self.currentVal
	
	def run(self):
		while not rospy.is_shutdown():
                        self.currentVal = self.session.next()
                        self.publish()
                        
        def publish(self):
		try:
			#print >> sys.stderr, type(self.currentVal['lat'])
                        #print >> sys.stderr, type(self.currentVal['lon'])
                        self.currentFixLL.latitude = self.currentVal['lat']
			self.currentFixLL.longitude = self.currentVal['lon']
                        self.currentFixLL.altitude = self.currentVal['alt']
                        self.currentFixForUTM.latitude = self.currentVal['lat']
                        self.currentFixForUTM.longitude = self.currentVal['lon']
                        self.currentFixForUTM.altitude = self.currentVal['alt']
                except Exception as err:
                        self.currentFixLL.latitude = 0
                        self.currentFixLL.longitude = 0
                        self.currentFixForUTM.latitude = 0
                        self.currentFixForUTM.longitude = 0
                        self.currentFixForUTM.altitude = 0
                        #print >>sys.stderr, err
		self.fixPublisherLL.publish(self.currentFixLL)
                self.fixPublisherUTM.publish(self.currentFixForUTM)

if __name__ == '__main__':
	gpsd = GPSD()
	try:
		gpsd.run()
	except rospy.ROSInterruptException: pass
	
