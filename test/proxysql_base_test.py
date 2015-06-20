import random
import re
import subprocess
import time
from unittest import TestCase

from docker import Client
from docker.utils import kwargs_from_env
import MySQLdb

class ProxySQLBaseTest(TestCase):

	DOCKER_COMPOSE_FILE = None
	PROXYSQL_ADMIN_PORT = 6032
	PROXYSQL_ADMIN_USERNAME = "admin"
	PROXYSQL_ADMIN_PASSWORD = "admin"
	PROXYSQL_RW_PORT = 6033
	PROXYSQL_RW_USERNAME = "root"
	PROXYSQL_RW_PASSWORD = "root"

	@classmethod
	def _startup_docker_services(cls):
		"""Start up all the docker services necessary to start this test.

		They are specified in the docker compose file specified in the variable
		cls.DOCKER_COMPOSE_FILE.
		"""

		# We have to perform docker-compose build + docker-compose up,
		# instead of just doing the latter because of a bug which will give a
		# 500 internal error for the Docker bug. When this is fixed, we should
		# remove this first extra step.
		subprocess.call(["docker-compose", "build"], cwd=cls.DOCKER_COMPOSE_FILE)
		subprocess.call(["docker-compose", "up", "-d"], cwd=cls.DOCKER_COMPOSE_FILE)

	@classmethod
	def _shutdown_docker_services(cls):
		"""Shut down all the docker services necessary to start this test.

		They are specified in the docker compose file specified in the variable
		cls.DOCKER_COMPOSE_FILE.
		"""

		subprocess.call(["docker-compose", "stop"], cwd=cls.DOCKER_COMPOSE_FILE)
		subprocess.call(["docker-compose", "rm", "--force"], cwd=cls.DOCKER_COMPOSE_FILE)

	@classmethod
	def _get_proxysql_container(cls):
		"""Out of all the started docker containers, select the one which
		represents the proxy instance.

		Note that this only supports one proxy instance for now. This method
		relies on interogating the Docker daemon via its REST API.
		"""

		containers = Client(**kwargs_from_env()).containers()
		for container in containers:
			if 'proxysql' in container['Image']:
				return container

	@classmethod
	def _get_mysql_containers(cls):
		"""Out of all the started docker containers, select the ones which
		represent the MySQL backend instances.

		This method relies on interogating the Docker daemon via its REST API.
		"""

		result = []
		containers = Client(**kwargs_from_env()).containers()
		for container in containers:
			if 'proxysql' not in container['Image']:
				result.append(container)
		return result

	@classmethod
	def _populate_mysql_containers_with_dump(cls):
		"""Populates the started MySQL backend containers with the specified
		SQL dump file.

		The reason for doing this __after__ the containers are started is
		because we want to keep them as generic as possible.
		"""

		mysql_containers = cls._get_mysql_containers()
		# We have already added the SQL dump to the container by using
		# the ADD mysql command in the Dockerfile for mysql -- check it
		# out. The standard agreed location is at /tmp/schema.sql.
		#
		# Unfortunately we can't do this step at runtime due to limitations
		# on how transfer between host and container is supposed to work by
		# design. See the Dockerfile for MySQL for more details.
		for mysql_container in mysql_containers:
			container_id = mysql_container['Names'][0][1:]
			subprocess.call(["docker", "exec", container_id, "bash", "/tmp/import_schema.sh"])

	@classmethod
	def _extract_hostgroup_from_container_name(cls, container_name):
		"""MySQL backend containers are named using a naming convention:
		backendXhostgroupY, where X and Y can be multi-digit numbers.
		This extracts the value of the hostgroup from the container name.

		I made this choice because I wasn't able to find another easy way to
		associate arbitrary metadata with a Docker container through the
		docker compose file.
		"""

		service_name = container_name.split('_')[1]
		return int(re.search(r'BACKEND(\d+)HOSTGROUP(\d+)', service_name).group(2))

	@classmethod
	def _extract_port_number_from_uri(cls, uri):
		"""Given a Docker container URI (exposed as an environment variable by
		the host linking mechanism), extract the TCP port number from it."""
		return int(uri.split(':')[2])

	@classmethod
	def _get_environment_variables_from_container(cls, container_name):
		"""Retrieve the environment variables from the given container.

		This is useful because the host linking mechanism will expose
		connectivity information to the linked hosts by the use of environment
		variables.
		"""

		output = Client(**kwargs_from_env()).execute(container_name, 'env')
		result = {}
		lines = output.split('\n')
		for line in lines:
			line = line.strip()
			if len(line) == 0:
				continue
			(k, v) = line.split('=')
			result[k] = v
		return result

	@classmethod
	def _populate_proxy_configuration_with_backends(cls):
		"""Populate ProxySQL's admin information with the MySQL backends
		and their associated hostgroups.

		This is needed because I do not want to hardcode this into the ProxySQL
		config file of the test scenario, as it leaves more room for quick
		iteration.

		In order to configure ProxySQL with the correct backends, we are using
		the MySQL admin interface of ProxySQL, and inserting rows into the
		`mysql_servers` table, which contains a list of which servers go into
		which hostgroup.
		"""
		proxysql_container = cls._get_proxysql_container()
		mysql_containers = cls._get_mysql_containers()
		environment_variables = cls._get_environment_variables_from_container(
											 proxysql_container['Names'][0][1:])

		proxy_admin_connection = MySQLdb.connect("127.0.0.1",
												cls.PROXYSQL_ADMIN_USERNAME,
												cls.PROXYSQL_ADMIN_PASSWORD,
												port=cls.PROXYSQL_ADMIN_PORT)
		cursor = proxy_admin_connection.cursor()

		for mysql_container in mysql_containers:
			container_name = mysql_container['Names'][0][1:].upper()
			port_uri = environment_variables['%s_PORT' % container_name]
			port_no = cls._extract_port_number_from_uri(port_uri)
			ip = environment_variables['%s_PORT_%d_TCP_ADDR' % (container_name, port_no)]
			hostgroup = cls._extract_hostgroup_from_container_name(container_name)
			cursor.execute("INSERT INTO mysql_servers(hostgroup_id, hostname, port, status) "
							"VALUES(%d, '%s', %d, 'ONLINE')" %
							(hostgroup, ip, port_no))

		cursor.execute("LOAD MYSQL SERVERS TO RUNTIME")
		cursor.close()
		proxy_admin_connection.close()

	@classmethod
	def setUpClass(cls):
		# Always shutdown docker services because the previous test might have
		# left them in limbo.
		cls._shutdown_docker_services()

		cls._startup_docker_services()

		# Sleep for 30 seconds because we want to populate the MySQL containers
		# with SQL dumps, but there is a race condition because we do not know
		# when the MySQL daemons inside them have actually started or not.
		# TODO(andrei): find a better solution
		time.sleep(30)
		cls._populate_mysql_containers_with_dump()

		cls._populate_proxy_configuration_with_backends()

	@classmethod
	def tearDownClass(cls):
		cls._shutdown_docker_services()
	
	def run_query_proxysql(self, query, db, return_result=True,
							username=None, password=None, port=None):
		"""Run a query against the ProxySQL proxy and optionally return its
		results as a set of rows."""
		username = username or ProxySQLBaseTest.PROXYSQL_RW_USERNAME
		password = password or ProxySQLBaseTest.PROXYSQL_RW_PASSWORD
		port = port or ProxySQLBaseTest.PROXYSQL_RW_PORT
		proxy_connection = MySQLdb.connect("127.0.0.1",
											username,
											password,
											port=port,
											db=db)
		cursor = proxy_connection.cursor()
		cursor.execute(query)
		if return_result:
			rows = cursor.fetchall()
		cursor.close()
		proxy_connection.close()
		if return_result:
			return rows

	def run_query_mysql(self, query, db, return_result=True, hostgroup=0,
					    username=None, password=None):
		"""Run a query against the MySQL backend and optionally return its
		results as a set of rows.

		IMPORTANT: since the queries are actually ran against the MySQL backend,
		that backend needs to expose its MySQL port to the outside through
		docker compose's port mapping mechanism.

		This will actually parse the docker-compose configuration file to
		retrieve the available backends and hostgroups and will pick a backend
		from the specified hostgroup."""

		# Figure out which are the containers for the specified hostgroup
		mysql_backends = ProxySQLBaseTest._get_mysql_containers()
		mysql_backends_in_hostgroup = []
		for backend in mysql_backends:
			container_name = backend['Names'][0][1:].upper()
			backend_hostgroup = ProxySQLBaseTest._extract_hostgroup_from_container_name(container_name)

			mysql_port_exposed=False
			if not backend.get('Ports'):
				continue
			for exposed_port in backend.get('Ports', []):
				if exposed_port['PrivatePort'] == 3306:
					mysql_port_exposed = True

			if backend_hostgroup == hostgroup and mysql_port_exposed:
				mysql_backends_in_hostgroup.append(backend)

		if len(mysql_backends_in_hostgroup) == 0:
			raise Exception('No backends with a publicly exposed port were '
							'found in hostgroup %d' % hostgroup)

		# Pick a random container, extract its connection details
		container = random.choice(mysql_backends_in_hostgroup)
		for exposed_port in container.get('Ports', []):
			if exposed_port['PrivatePort'] == 3306:
				mysql_port = exposed_port['PublicPort']

		username = username or ProxySQLBaseTest.PROXYSQL_RW_USERNAME
		password = password or ProxySQLBaseTest.PROXYSQL_RW_PASSWORD
		mysql_connection = MySQLdb.connect("127.0.0.1",
											username,
											password,
											port=mysql_port,
											db=db)
		cursor = mysql_connection.cursor()
		cursor.execute(query)
		if return_result:
			rows = cursor.fetchall()
		cursor.close()
		mysql_connection.close()
		if return_result:
			return rows

	def run_sysbench_proxysql(self, threads=4, time=60, db="test",
								username=None, password=None, port=None):
		proxysql_container_id = ProxySQLBaseTest._get_proxysql_container()['Id']
		username = username or ProxySQLBaseTest.PROXYSQL_RW_USERNAME
		password = password or ProxySQLBaseTest.PROXYSQL_RW_PASSWORD
		port = port or ProxySQLBaseTest.PROXYSQL_RW_PORT

		params = [
					"docker", "exec", proxysql_container_id,
				 	"sysbench",
					 "--test=/opt/sysbench/sysbench/tests/db/oltp.lua",
					 "--num-threads=%d" % threads,
					 "--max-requests=0",
					 "--max-time=%d" % time,
					 "--mysql-user=%s" % username,
					 "--mysql-password=%s" % password,
					 "--mysql-db=%s" % db,
					 "--db-driver=mysql",
					 "--oltp-tables-count=4",
					 "--oltp-read-only=on",
					 "--oltp-skip-trx=on",
					 "--report-interval=1",
					 "--oltp-point-selects=100",
					 "--oltp-table-size=400000",
					 "--mysql-host=127.0.0.1",
					 "--mysql-port=%s" % port
				 ]
		subprocess.call(params + ["prepare"])
		subprocess.call(params + ["run"])
		subprocess.call(params + ["cleanup"])