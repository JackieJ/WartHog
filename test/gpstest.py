import time

from gps import *
session = gps()
#session = gps(**opts)
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
#for report in session:
#	print report
while True:
	print '_----'
	print session
	s = session.next()
	print s.keys()
	try:
		print s['lat'], s['lon']
	except:
		pass
		#print s
	time.sleep(.5)
