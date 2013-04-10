# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "wiimote: 3 messages, 0 services")

set(MSG_I_FLAGS "-Iwiimote:/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg;-Igeometry_msgs:/opt/ros/groovy/share/geometry_msgs/msg;-Istd_msgs:/opt/ros/groovy/share/std_msgs/msg;-Isensor_msgs:/opt/ros/groovy/share/sensor_msgs/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

#better way to handle this?
set (ALL_GEN_OUTPUT_FILES_cpp "")

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wiimote
)
_generate_msg_cpp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/State.msg
  "${MSG_I_FLAGS}"
  "/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg;/opt/ros/groovy/share/geometry_msgs/msg/Vector3.msg;/opt/ros/groovy/share/std_msgs/msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wiimote
)
_generate_msg_cpp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/TimedSwitch.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wiimote
)

### Generating Services

### Generating Module File
_generate_module_cpp(wiimote
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wiimote
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(wiimote_gencpp ALL
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wiimote
)
_generate_msg_lisp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/State.msg
  "${MSG_I_FLAGS}"
  "/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg;/opt/ros/groovy/share/geometry_msgs/msg/Vector3.msg;/opt/ros/groovy/share/std_msgs/msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wiimote
)
_generate_msg_lisp(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/TimedSwitch.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wiimote
)

### Generating Services

### Generating Module File
_generate_module_lisp(wiimote
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wiimote
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(wiimote_genlisp ALL
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
)
_generate_msg_py(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/State.msg
  "${MSG_I_FLAGS}"
  "/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/IrSourceInfo.msg;/opt/ros/groovy/share/geometry_msgs/msg/Vector3.msg;/opt/ros/groovy/share/std_msgs/msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
)
_generate_msg_py(wiimote
  /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/msg/TimedSwitch.msg
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
)

### Generating Services

### Generating Module File
_generate_module_py(wiimote
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(wiimote_genpy ALL
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)


debug_message(2 "wiimote: Iflags=${MSG_I_FLAGS}")


if(gencpp_INSTALL_DIR)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wiimote
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(wiimote_gencpp geometry_msgs_gencpp)
add_dependencies(wiimote_gencpp std_msgs_gencpp)
add_dependencies(wiimote_gencpp sensor_msgs_gencpp)

if(genlisp_INSTALL_DIR)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wiimote
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(wiimote_genlisp geometry_msgs_genlisp)
add_dependencies(wiimote_genlisp std_msgs_genlisp)
add_dependencies(wiimote_genlisp sensor_msgs_genlisp)

if(genpy_INSTALL_DIR)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
    DESTINATION ${genpy_INSTALL_DIR}
    # skip all init files
    PATTERN "__init__.py" EXCLUDE
    PATTERN "__init__.pyc" EXCLUDE
  )
  # install init files which are not in the root folder of the generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wiimote
    DESTINATION ${genpy_INSTALL_DIR}
    FILES_MATCHING
    REGEX "/wiimote/.+/__init__.pyc?$"
  )
endif()
add_dependencies(wiimote_genpy geometry_msgs_genpy)
add_dependencies(wiimote_genpy std_msgs_genpy)
add_dependencies(wiimote_genpy sensor_msgs_genpy)
