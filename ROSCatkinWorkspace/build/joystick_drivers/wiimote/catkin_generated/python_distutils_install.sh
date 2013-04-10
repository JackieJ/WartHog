#!/bin/sh -x

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

cd "/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote"

# todo --install-layout=deb per platform
# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/robo/Projects/ROSCatkinWorkspace/install/lib/python2.7/dist-packages:/home/robo/Projects/ROSCatkinWorkspace/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/robo/Projects/ROSCatkinWorkspace/build" \
    "/usr/bin/python" \
    "/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/setup.py" \
    build --build-base "/home/robo/Projects/ROSCatkinWorkspace/build/joystick_drivers/wiimote" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/robo/Projects/ROSCatkinWorkspace/install" --install-scripts="/home/robo/Projects/ROSCatkinWorkspace/install/bin"
