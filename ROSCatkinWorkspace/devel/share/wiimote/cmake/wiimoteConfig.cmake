# generated from catkin/cmake/template/pkgConfig.cmake.in

# append elements to a list if they are not already in the list
# copied from catkin/cmake/list_append_unique.cmake to keep pkgConfig
# self contained
macro(_list_append_unique listname)
  foreach(_item ${ARGN})
    list(FIND ${listname} ${_item} _index)
    if(_index EQUAL -1)
      list(APPEND ${listname} ${_item})
    endif()
  endforeach()
endmacro()

# remove duplicate libraries, generalized from PCLConfig.cmake.in
macro(_remove_duplicate_libraries _unfiltered_libraries _final_filtered_libraries)
  set(_filtered_libraries)
  set(_debug_libraries)
  set(_optimized_libraries)
  set(_other_libraries)
  set(_waiting_for_debug 0)
  set(_waiting_for_optimized 0)
  set(_library_position -1)
  foreach(library ${${_unfiltered_libraries}})
    if("${library}" STREQUAL "debug")
      set(_waiting_for_debug 1)
    elseif("${library}" STREQUAL "optimized")
      set(_waiting_for_optimized 1)
    elseif(_waiting_for_debug)
      list(FIND _debug_libraries "${library}" library_position)
      if(library_position EQUAL -1)
        list(APPEND ${_filtered_libraries} debug ${library})
        list(APPEND _debug_libraries ${library})
      endif()
      set(_waiting_for_debug 0)
    elseif(_waiting_for_optimized)
      list(FIND _optimized_libraries "${library}" library_position)
      if(library_position EQUAL -1)
        list(APPEND ${_filtered_libraries} optimized ${library})
        list(APPEND _optimized_libraries ${library})
      endif()
      set(_waiting_for_optimized 0)
    else("${library}" STREQUAL "debug")
      list(FIND _other_libraries "${library}" library_position)
      if(library_position EQUAL -1)
        list(APPEND ${_filtered_libraries} ${library})
        list(APPEND _other_libraries ${library})
      endif()
    endif("${library}" STREQUAL "debug")
  endforeach(library)
  set(_final_filtered_libraries _filtered_libraries)
endmacro()


if(wiimote_CONFIG_INCLUDED)
  return()
endif()
set(wiimote_CONFIG_INCLUDED TRUE)

# set variables for source/devel/install prefixes
if(TRUE)
  set(wiimote_SOURCE_PREFIX /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote)
  set(wiimote_DEVEL_PREFIX /home/robo/Projects/ROSCatkinWorkspace/devel)
  set(wiimote_INSTALL_PREFIX "")
  set(wiimote_PREFIX ${wiimote_DEVEL_PREFIX})
else()
  set(wiimote_SOURCE_PREFIX "")
  set(wiimote_DEVEL_PREFIX "")
  set(wiimote_INSTALL_PREFIX /home/robo/Projects/ROSCatkinWorkspace/install)
  set(wiimote_PREFIX ${wiimote_INSTALL_PREFIX})
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "WARNING: package 'wiimote' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  message("${_msg}")
endif()

# flag project as catkin-based to distinguish if a find_package()-ed project is a catkin project
set(wiimote_FOUND_CATKIN_PROJECT TRUE)

if(NOT "/home/robo/Projects/ROSCatkinWorkspace/devel/include" STREQUAL "")
  set(wiimote_INCLUDE_DIRS "")
  set(absolute_include_dirs "/home/robo/Projects/ROSCatkinWorkspace/devel/include")
  foreach(idir ${absolute_include_dirs})
    if(IS_ABSOLUTE ${idir} AND IS_DIRECTORY ${idir})
      set(include ${idir})
    elseif(IS_DIRECTORY /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/${idir})
      set(include /home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/${idir})
    else()
      message(FATAL_ERROR "Project 'wiimote' specifies '${idir}' as an include dir, which is not found.  It does neither exist as an absolute directory nor in '/home/robo/Projects/ROSCatkinWorkspace/src/joystick_drivers/wiimote/${idir}'.  Ask the maintainer 'Jonathan Bohren <jbo@jhu.edu>' to fix it.")
    endif()
    _list_append_unique(wiimote_INCLUDE_DIRS ${include})
  endforeach()
endif()

set(libraries "")
foreach(library ${libraries})
  if(TARGET ${library})
    list(APPEND wiimote_LIBRARIES ${library})
  elseif(IS_ABSOLUTE ${library})
    list(APPEND wiimote_LIBRARIES ${library})
  else()
    set(lib_path "")
    set(lib "${library}-NOTFOUND")
    # since the path where the library is found is returned we have to iterate over the paths manually
    foreach(path /home/robo/Projects/ROSCatkinWorkspace/devel/lib;/opt/ros/groovy/lib)
      find_library(lib ${library}
        PATHS ${path}
        NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
      if(lib)
        set(lib_path ${path})
        break()
      endif()
    endforeach()
    if(lib)
      _list_append_unique(wiimote_LIBRARY_DIRS ${lib_path})
      list(APPEND wiimote_LIBRARIES ${lib})
    else()
      # as a fall back for non-catkin libraries try to search globally
      find_library(lib ${library})
      if(NOT lib)
        message(FATAL_ERROR "Project '${PROJECT_NAME}' tried to find library '${library}'.  The library is neither a target nor built/installed properly.  Did you compile project 'wiimote'?  Did you find_package() it before the subdirectory containing its code is included?")
      endif()
      list(APPEND wiimote_LIBRARIES ${lib})
    endif()
  endif()
endforeach()

set(wiimote_EXPORTED_TARGETS "")
# create dummy targets for exported code generation targets to make life of users easier
foreach(t ${wiimote_EXPORTED_TARGETS})
  if(NOT TARGET ${t})
    add_custom_target(${t})
  endif()
endforeach()

set(depends "geometry_msgs;sensor_msgs;std_msgs;std_srvs;rospy;roslib;genmsg")
foreach(depend ${depends})
  string(REPLACE " " ";" depend_list ${depend})
  # the package name of the dependency must be kept in a unique variable so that it is not overwritten in recursive calls
  list(GET depend_list 0 wiimote_dep)
  list(LENGTH depend_list count)
  if(${count} EQUAL 1)
    # simple dependencies must only be find_package()-ed once
    if(NOT ${wiimote_dep}_FOUND)
      find_package(${wiimote_dep} REQUIRED)
    endif()
  else()
    # dependencies with components must be find_package()-ed again
    list(REMOVE_AT depend_list 0)
    find_package(${wiimote_dep} REQUIRED ${depend_list})
  endif()
  _list_append_unique(wiimote_INCLUDE_DIRS ${${wiimote_dep}_INCLUDE_DIRS})
  list(APPEND wiimote_LIBRARIES ${${wiimote_dep}_LIBRARIES})
  _list_append_unique(wiimote_LIBRARY_DIRS ${${wiimote_dep}_LIBRARY_DIRS})
  list(APPEND wiimote_EXPORTED_TARGETS ${${wiimote_dep}_EXPORTED_TARGETS})
endforeach()

if(wiimote_LIBRARIES)
  _remove_duplicate_libraries(wiimote_LIBRARIES wiimote_LIBRARIES)
endif()

set(pkg_cfg_extras "")
foreach(extra ${pkg_cfg_extras})
  if(NOT IS_ABSOLUTE ${extra})
    set(extra ${wiimote_DIR}/${extra})
  endif()
  include(${extra})
endforeach()