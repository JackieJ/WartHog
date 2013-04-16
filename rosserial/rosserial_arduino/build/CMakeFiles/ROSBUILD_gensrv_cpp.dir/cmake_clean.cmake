FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/rosserial_arduino/msg"
  "../src/rosserial_arduino/srv"
  "CMakeFiles/ROSBUILD_gensrv_cpp"
  "../srv_gen/cpp/include/rosserial_arduino/Test.h"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_cpp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
