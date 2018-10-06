
# MySQL Database Driver

import MySQLdb as mdb
import config.config as config
from data_store.database_driver.base_database_driver import BaseDatabaseDriver
from utils.print import ppp

import time


class MySqlDriver(BaseDatabaseDriver):
	"""
	MySQL database driver which implements CRUD and utility public methods.

	TODO:
		- add docstrings to new methods
		- order by, ascending and descending
		- transactions
		- type checking, type consistency

	"""

	RECORD_UUID_COLUMN = 'uuid'
	RECORD_CREATED_TS_COLUMN = 'created_ts'
	RECORD_UPDATED_TS_COLUMN = 'updated_ts'

	REQUIRED_RECORD_PROPERTIES = [
		RECORD_UUID_COLUMN
	]

	IMMUTABLE_RECORD_PROPERTIES = [
		RECORD_UUID_COLUMN,
		RECORD_CREATED_TS_COLUMN
	]

	WHERE_MAP = {
		'=': '=',
		'!=': '<>',
		'lt': '<',
		'<': '<',
		'gt': '>',
		'>': '>',
		'lte': '<=',
		'<=': '<=',
		'gte': '>=',
		'>=': '>=',
		'is': 'IS',
		'is not': 'IS NOT',
		'like': 'LIKE',
		'not like': 'NOT LIKE'
	}

	WHERE_IN_MAP = {
		'in': 'IN',
		'not in': 'NOT IN'
	}


	def __init__(self, database_name):
		"""
		MySQL driver instance constructor.

		Sets database name and configures the MySQL server connection and
		cursor.

		Args:
			database_name (str): Name of MySQL database.

		"""

		self.database_name = self.escape(database_name)
		self.conn = mdb.connect(
			host=config.MYSQL_HOST,
			user=config.MYSQL_USER,
			passwd=config.MYSQL_PASSWORD,
			db=database_name
		)
		self.cur = self.conn.cursor(mdb.cursors.DictCursor)
		self.conn.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')


	########## CRUD INTERFACE METHODS ##########


	def insert(self, table_name, value_props={}):
		"""
		MySQL driver interface method for single record inserts.

		Args:
			table_name (str): Name of MySQL table.
			value_props (dict): Dictionary of column insert values where
				key=column name and value=column value.

		Returns:
			(dict) Dictionary representing MySQL record or None if insert is
				unsuccessful.

		"""

		# validate value_props for necessary items
		if not self.validate_record_props(value_props):
			raise RuntimeError("invalid record properties for INSERT")

		# set 'created' and 'updated' record metadata
		value_props[self.RECORD_CREATED_TS_COLUMN] = self.get_curr_timestamp()
		value_props[self.RECORD_UPDATED_TS_COLUMN] = self.get_curr_timestamp()

		# gather fields and values for record data
		fields = []
		values = []
		for key, val in value_props.items():
			fields.append(key)
			values.append(val)

		# construct fields and values substring
		fields_str = ', '.join([
			"`{}`".format(self.escape(field))
			for field in fields
		])
		values_str_sub = ', '.join(['%s' for item in values])

		# construct full insert SQL string
		query_stmt = """
			INSERT INTO `{0}` ({1})
			VALUES ({2});
		""".format(
			self.escape(table_name),
			fields_str,
			values_str_sub
		)

		# commit the insert to the table
		with self.conn:
			insert_count = self.cur.execute(query_stmt, tuple(values))
			self.conn.commit()
			if self.cur.rowcount == 1:
				return value_props
			else:
				return None


	def find_by_uuid(self, table_name, uuid):
		records = self.find_by_fields(
			table_name=table_name,
			where_props={ self.RECORD_UUID_COLUMN: uuid }
		)
		if len(records) > 0:
			return records[0]


	def find_by_fields(self, table_name, where_props={}, limit=None):
		"""
		MySQL driver interface method for finding records by conditionals.

		Args:
			table_name (str): Name of MySQL table.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.
			limit (int or None): Positive integer limit for query results list.

		Returns:
			(tuple) Tuple of dictionaries representing MySQL records.

		"""

		query_stmt_components = []

		# add SELECT query component
		select_component = 'SELECT * FROM `{}`'.format(
			self.escape(table_name)
		)
		query_stmt_components.append(select_component)

		# add WHERE query components
		where_values = None
		if len(where_props.keys()) > 0:
			where_component, where_values = self.construct_where_clause(
				where_props=where_props
			)
			query_stmt_components.append(where_component)
			where_values = tuple(where_values)

		# add LIMIT query component
		if(limit is not None and int(limit) > 0):
			limit_component = 'LIMIT {}'.format(self.escape(str(limit)))
			query_stmt_components.append(limit_component)

		# join query components together to create entire statement
		query_stmt = ' '.join(query_stmt_components) + ';'

		# execute the query and return the results
		with self.conn:
			if where_values is not None:
				self.cur.execute(query_stmt, where_values)
			else:
				self.cur.execute(query_stmt)
			return self.cur.fetchall()


	def update_by_uuid(self, table_name, uuid, value_props={}):
		return self.update_by_fields(
			table_name=table_name,
			value_props=value_props,
			where_props={ self.RECORD_UUID_COLUMN: uuid }
		)


	def update_by_fields(self, table_name, value_props={}, where_props={}):
		"""
		MySQL driver interface method for updating records by conditionals.

		Args:
			table_name (str): Name of MySQL table.
			value_props (dict): Dictionary of column update values where
				key=column name and value=column value.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.

		Returns:
			{
				'rows_affected': (integer) Number of rows updated,
				'updated_ts': (integer) Current timestamp
			}

		"""

		res = {}

		# filter immutable properties from value_props
		unfiltered_value_props = value_props
		value_props = {}
		for key, val in unfiltered_value_props.items():
			if key not in self.IMMUTABLE_RECORD_PROPERTIES:
				value_props[key] = val

		# mutate 'updated_ts' column to current time on update
		current_timestamp = self.get_curr_timestamp()
		value_props[self.RECORD_UPDATED_TS_COLUMN] = current_timestamp

		# start gathering query parts
		query_stmt_components = []

		# add the UPDATE component
		update_component = 'UPDATE `{}`'.format(
			self.escape(table_name)
		)
		query_stmt_components.append(update_component)

		# add the SET component
		set_values = None
		if len(value_props.keys()) > 0:
			set_fields = []
			set_values = []
			for key, val in value_props.items():
				set_fields.append(key)
				set_values.append(val)
			set_component = 'SET ' + ', '.join([
				'`{}`=%s'.format(self.escape(field))
				for field in set_fields
			])
			query_stmt_components.append(set_component)
		else:
			raise RuntimeError(
				"argument 'value_props' required with at least one SET item"
			)

		# add the WHERE component
		where_values = None
		if len(where_props.keys()) > 0:
			where_component, where_values = self.construct_where_clause(
				where_props=where_props
			)
			query_stmt_components.append(where_component)
		else:
			raise RuntimeError(
				"argument 'where_props' required with at least one WHERE " +
				"condition"
			)

		# join the query components together
		query_stmt = ' '.join(query_stmt_components) + ';'

		# commit the update to the datastore
		with self.conn:
			self.cur.execute(query_stmt, tuple(set_values + where_values))
			res[self.RECORD_UPDATED_TS_COLUMN] = current_timestamp
			res['rows_affected'] = self.cur.rowcount
			return res


	def delete_by_uuid(self, table_name, uuid):
		return self.delete_by_fields(
			table_name=table_name,
			where_props={ self.RECORD_UUID_COLUMN: uuid }
		)


	def delete_by_fields(self, table_name, where_props={}):
		"""
		MySQL driver interface method for deleting records by conditionals.

		Args:
			table_name (str): Name of MySQL table.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.

		Returns:
			(integer) Number of rows deleted.

		"""

		query_stmt_components = []

		# add the DELETE component
		delete_component = 'DELETE FROM `{}`'.format(
			self.escape(table_name)
		)
		query_stmt_components.append(delete_component)

		# add the WHERE components
		where_values = None
		if len(where_props.keys()) > 0:
			where_component, where_values = self.construct_where_clause(
				where_props=where_props
			)
			query_stmt_components.append(where_component)
		else:
			# don't allow DELETE without at least one WHERE condition
			raise RuntimeError(
				"""
					argument 'where_props' required with at least one WHERE
					condition
				"""
			)

		# join the query components together
		query_stmt = ' '.join(query_stmt_components) + ';'

		# execute the query and return the number of deleted records
		with self.conn:
			self.cur.execute(query_stmt, tuple(where_values))
			return self.cur.rowcount


	########## MYSQL SPECIFIC METHODS ##########


	def query_bind(self, query_string, bind_vars={}):
		"""
		Performs a MySQL query from a raw query string and returns the result.
		Uses bound variables to protect against SQL injection.

		Args:
			query_string (str): formatted MySQL query string.
				Ex. 'SELECT * FROM table where id=:id'
			bind_vars (dict): named variables to be escaped and injected into
				the query string.
				Ex. { 'id': 1234 }

		Returns:
			(tuple) Tuple of dictionary representations of records.

		"""

		for key, val in bind_vars.items():
			bind_str = ':{0}'.format(key)
			if bind_str in query_string:
				query_string = query_string.replace(
					bind_str,
					'%({0})s'.format(key)
				)
		self.cur.execute(query_string, bind_vars)
		return self.cur.fetchall()


	########## TABLE UTILITIES ##########


	def describe_table(self, table_name):
		query_stmt = "DESC {};".format(
			self.escape(table_name)
		)
		with self.conn:
			self.cur.execute(query_stmt)
		return self.cur.fetchall()


	def get_table_field_names(self, table_name):
		table_desc = self.describe_table(table_name=table_name)
		field_names = [col['Field'] for col in table_desc]
		return field_names


	########## DATABASE UTILITIES ##########


	def get_database_size(self):
		query_stmt = """
			SELECT table_name AS "Table",
			ROUND(((data_length + index_length) / 1024 / 1024), 2)
			AS "Size (MB)"
			FROM information_schema.TABLES
			WHERE table_schema = "{}"
			ORDER BY (data_length + index_length) DESC;
		""".format(self.database_name)
		with self.conn:
			self.cur.execute(query_stmt)
		return self.cur.fetchall()


	########## SQL UTILITIES ##########


	@staticmethod
	def escape(string):
		"""
		Escape strings for use in query strings.

		"""

		return mdb.escape_string(string).decode('utf-8')


	@staticmethod
	def get_curr_timestamp():
		"""
		Get timestamp for current time.

		"""

		return int(time.time())


	@classmethod
	def validate_record_props(self, value_props):
		"""
		Ensure required record properties exist.

		"""

		for property_name in self.REQUIRED_RECORD_PROPERTIES:
			if property_name not in value_props:
				return False
		return True


	@classmethod
	def construct_where_clause(cls, where_props={}):
		"""
		'WHERE' clause string builder with parameter bindings.

		"""

		where_strings = []
		where_values = []
		for prop_col, prop_cond in where_props.items():
			if type(prop_cond) is dict:
				for cond_key, cond_val in prop_cond.items():
					if cond_key in cls.WHERE_MAP:
						s = '`{0}` {1} %s'.format(
							cls.escape(prop_col),
							cls.WHERE_MAP[cond_key],
						)
						where_strings.append(s)
						where_values.append(cond_val)
					elif cond_key in cls.WHERE_IN_MAP and \
					type(cond_val) is list:
						s = '`{0}` {1} ({2})'.format(
							cls.escape(prop_col),
							cls.WHERE_IN_MAP[cond_key],
							','.join(['%s' for x in cond_val])
						)
						where_strings.append(s)
						where_values = where_values + cond_val
					else:
						raise RuntimeError("invalid WHERE conditional")
			else:
				if prop_cond is None:
					s = '`{0}` IS %s'.format(cls.escape(prop_col))
				else:
					s = '`{0}` = %s'.format(cls.escape(prop_col))
				where_strings.append(s)
				where_values.append(prop_cond)

		where_component = 'WHERE ' + ' AND '.join(where_strings)
		return where_component, where_values

