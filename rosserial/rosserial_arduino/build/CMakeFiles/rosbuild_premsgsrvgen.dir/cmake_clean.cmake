FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/rosserial_arduino/msg"
  "../src/rosserial_arduino/srv"
  "CMakeFiles/rosbuild_premsgsrvgen"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/rosbuild_premsgsrvgen.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
