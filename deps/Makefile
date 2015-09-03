

default: libevent libconfig libdaemon jemalloc mariadb_client re2 libinjection
.PHONY: default

libdaemon/libdaemon/libdaemon/.libs/libdaemon.a: 
	cd libdaemon/libdaemon && ./configure
	cd libdaemon/libdaemon && make

libdaemon: libdaemon/libdaemon/libdaemon/.libs/libdaemon.a

libevent/libevent/.libs/libevent.a:
	cd libevent/libevent && ./configure
	cd libevent/libevent && make

libevent: libevent/libevent/.libs/libevent.a

libinjection/libinjection.a:
	cd libinjection && make

libinjection: libinjection/libinjection.a

jemalloc/jemalloc/lib/libjemalloc.a:
	cd jemalloc/jemalloc && ./configure --enable-xmalloc
	cd jemalloc/jemalloc && make

jemalloc: jemalloc/jemalloc/lib/libjemalloc.a

mariadb-client-library/mariadb_client/include/my_config.h:
	cd mariadb-client-library/mariadb_client && cmake .
	cd mariadb-client-library/mariadb_client && make

mariadb_client: mariadb-client-library/mariadb_client/include/my_config.h

libconfig/libconfig/lib/.libs/libconfig++.a:
	cd libconfig/libconfig && ./configure
	cd libconfig/libconfig && make

libconfig: libconfig/libconfig/lib/.libs/libconfig++.a

re2/re2/obj/libre2.a:
	cd re2/re2 && sed -i -e 's/-O3 -g /-O3 -fPIC /' Makefile
	cd re2/re2 && make

re2: re2/re2/obj/libre2.a

cleanall:
	cd libdaemon/libdaemon && make clean
	cd libevent/libevent && make clean
	cd libinjection && make clean
	cd jemalloc/jemalloc && make clean
	cd mariadb-client-library && make clean
	cd libconfig && make clean
	cd re2 && make clean

.PHONY: cleanall

