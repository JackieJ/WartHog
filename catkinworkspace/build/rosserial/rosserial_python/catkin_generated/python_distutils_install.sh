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

cd "/home/robo/Projects/WartHog/catkinworkspace/src/rosserial/rosserial_python"

# todo --install-layout=deb per platform
# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/robo/Projects/WartHog/catkinworkspace/install/lib/python2.7/dist-packages:/home/robo/Projects/WartHog/catkinworkspace/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/robo/Projects/WartHog/catkinworkspace/build" \
    "/usr/bin/python" \
    "/home/robo/Projects/WartHog/catkinworkspace/src/rosserial/rosserial_python/setup.py" \
    build --build-base "/home/robo/Projects/WartHog/catkinworkspace/build/rosserial/rosserial_python" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/robo/Projects/WartHog/catkinworkspace/install" --install-scripts="/home/robo/Projects/WartHog/catkinworkspace/install/bin"
