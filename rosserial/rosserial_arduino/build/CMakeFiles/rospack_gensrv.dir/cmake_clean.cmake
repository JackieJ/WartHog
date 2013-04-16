FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/rosserial_arduino/msg"
  "../src/rosserial_arduino/srv"
  "CMakeFiles/rospack_gensrv"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/rospack_gensrv.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
