import time
import os

from gps import *

session = gps(WATCH_ENABLE)
#session = gps(**opts)
#session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
#for report in session:
# print report
print session
print session.next()
print session.next()
print session.next()
print session.next()
while True:
    print '_----'
    print session
    s = session.next()
    print s.keys()
