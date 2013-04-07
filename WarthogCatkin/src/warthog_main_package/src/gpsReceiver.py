#!/usr/bin/python

import time
import sys
from gps import *

import roslib; roslib.load_manifest('gps_common')
import rospy
from  gps_common.msg import *

class GPSD():
	def __init__(self):
		rospy.init_node('GPSD')
                self.session = gps()
		self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
		self.currentVal = None
		self.fixPublisher = rospy.Publisher('fix', GPSFix)
	def get_currentVal(self):
		return self.currentVal
	
	def run(self):
		while not rospy.is_shutdown():
                        while True:
                                self.currentVal = self.session.next()
                                self.publish()
        def publish(self):
		try:
			#print >> sys.stderr, type(self.currentVal['lat'])
                        #print >> sys.stderr, type(self.currentVal['lon'])
                        self.currentFix.latitude = self.currentVal['lat']
			self.currentFix.longitude = self.currentVal['lon']
                except Exception as err:
                        self.currentFix.latitude = 0
                        self.currentFix.latitude = 0
                        #print >>sys.stderr, err
		self.fixPublisher.publish(self.currentFix)
                
if __name__ == '__main__':
	gpsd = GPSD()
	try:
		gpsd.run()
	except rospy.ROSInterruptException: pass
	
