#!/usr/bin/env python
#Author: Jackie Jin
#Des: interface with gpsd
import sys
import time
from gps import *

class GPSD():
 def __init__(self):
  self.session = gps()
  self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
  self.currentVal = None
        
 def run(self):
  while not rospy.is_shutdown():
   while True:
    self.currentVal = self.session.next()
    print >> sys.stderr, self.currentVal


if __name__ == '__main__':
 gpsd = GPSD()
 try: 
  gpsd.run()
 except rospy.ROSInterrupException: pass
