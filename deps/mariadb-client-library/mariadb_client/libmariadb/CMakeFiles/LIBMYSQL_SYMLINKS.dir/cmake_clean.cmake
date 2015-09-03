FILE(REMOVE_RECURSE
  "CMakeFiles/LIBMYSQL_SYMLINKS"
  "libmysql.dylib"
  "libmysqlclient.dylib"
  "libmysqlclient_r.dylib"
  "libmysqlclient.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/LIBMYSQL_SYMLINKS.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
