FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/rosserial_arduino/msg"
  "../src/rosserial_arduino/srv"
  "CMakeFiles/ROSBUILD_gensrv_py"
  "../src/rosserial_arduino/srv/__init__.py"
  "../src/rosserial_arduino/srv/_Test.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
