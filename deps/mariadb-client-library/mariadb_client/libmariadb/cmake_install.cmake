# Install script for directory: /Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Relwithdebinfo")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/mariadb" TYPE SHARED_LIBRARY FILES
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmariadb.2.dylib"
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmariadb.dylib"
    )
  FOREACH(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/mariadb/libmariadb.2.dylib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/mariadb/libmariadb.dylib"
      )
    IF(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      EXECUTE_PROCESS(COMMAND "/usr/bin/install_name_tool"
        -id "libmariadb.2.dylib"
        "${file}")
      IF(CMAKE_INSTALL_DO_STRIP)
        EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "${file}")
      ENDIF(CMAKE_INSTALL_DO_STRIP)
    ENDIF()
  ENDFOREACH()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/mariadb" TYPE STATIC_LIBRARY FILES "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmariadbclient.a")
  IF(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/mariadb/libmariadbclient.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/mariadb/libmariadbclient.a")
    EXECUTE_PROCESS(COMMAND "/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/mariadb/libmariadbclient.a")
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/mariadb" TYPE FILE FILES
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmysql.dylib"
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmysqlclient.dylib"
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmysqlclient_r.dylib"
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/libmariadb/libmysqlclient.a"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/mariadb" TYPE DIRECTORY FILES "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/include/")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/mariadb" TYPE FILE FILES
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/include/my_config.h"
    "/Users/aismail/proxysql-0.2/deps/mariadb-client-library/mariadb_client/include/mysql_version.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

