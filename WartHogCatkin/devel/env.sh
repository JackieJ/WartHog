#!/usr/bin/env sh
# generated from catkin/cmake/templates/env.sh.in

if [ $# -eq 0 ] ; then
  /bin/echo "Entering environment at '/home/jackie/Projects/WartHog/WartHogCatkin/devel', type 'exit' to leave"
  . "/home/jackie/Projects/WartHog/WartHogCatkin/devel/setup.sh"
  "$SHELL" -i
  /bin/echo "Exiting environment at '/home/jackie/Projects/WartHog/WartHogCatkin/devel'"
else
  . "/home/jackie/Projects/WartHog/WartHogCatkin/devel/setup.sh"
  exec "$@"
fi
