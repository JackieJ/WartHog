import time

from gps import *
session = gps()
#session = gps(**opts)
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
#for report in session:
#	print report
# print session
# print session.next()
# print session.next()
# print session.next()
# print session.next()
while True:
	#print '_----'
	s = session.next()
        print s
        try:
                print s['lat'], s['lon']
	except:
		pass
		#print s
	time.sleep(.5)
