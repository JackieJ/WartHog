#!/usr/bin/python

import time
import sys
from gps import *
import yaml

class GPSD():
	def __init__(self):
                self.session = gps()
		self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
		self.currentVal = None
                self.result = None
                self.rList = []
	
        def get_currentVal(self):
		return self.currentVal
	
	def run(self):
		while True:
                        self.currentVal = self.session.next()
                        self.collect()
                        time.sleep(0.5)
                                
        def collect(self):
                try:
                        print >> sys.stderr, self.currentVal['lat']
                        print >> sys.stderr, self.currentVal['lon']
                        self.result.longitude = self.currentVal['lon']
                        self.result.latitude = self.currentVal['lat']
                        rList.append(result)
                except Exception as err:
                        print >> sys.stderr, "no lon lat reading yet!"
        
        def dumpToFile(self):
                file = open('./src/waypoints.yaml', "w+")
                yaml.dump(rList, file)

if __name__ == '__main__':
	gpsd = GPSD()
	try:
		gpsd.run()
	except KeyboardInterrupt: 
                pass
	
