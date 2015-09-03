FILE(REMOVE_RECURSE
  "libmariadb.pdb"
  "libmariadb.dylib"
  "libmariadb.2.dylib"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/libmariadb.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
