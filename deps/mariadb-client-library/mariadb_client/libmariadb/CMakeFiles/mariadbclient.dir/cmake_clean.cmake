FILE(REMOVE_RECURSE
  "libmariadbclient.pdb"
  "libmariadbclient.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/mariadbclient.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
