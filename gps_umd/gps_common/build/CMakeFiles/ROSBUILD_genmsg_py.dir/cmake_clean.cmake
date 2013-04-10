FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/gps_common/msg"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/gps_common/msg/__init__.py"
  "../src/gps_common/msg/_GPSStatus.py"
  "../src/gps_common/msg/_GPSFix.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
