
# MySQL Database Driver

import MySQLdb as mdb
import config.config as config
from data_store.database_driver.base_driver import BaseDriver
from utils.print import ppp

import time


class MySqlDriver(BaseDriver):
	"""
	MySQL database driver which implements CRUD and utility public methods.

	TODO:
		- add 'WHERE' clause string builder
	"""


	RECORD_CREATED_TS_COLUMN = 'created_ts'
	RECORD_UPDATED_TS_COLUMN = 'updated_ts'


	def __init__(self, database_name):
		self.database_name = self.__escape(database_name)
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
			(integet) 'id' of the inserted record.

		"""

		value_props[self.RECORD_CREATED_TS_COLUMN] = int(time.time())
		value_props[self.RECORD_UPDATED_TS_COLUMN] = int(time.time())

		fields = []
		values = []
		for key, val in value_props.items():
			fields.append(key)
			values.append(val)

		fields_str = ', '.join([
			"`{}`".format(self.__escape(field))
			for field in fields
		])
		values_str_sub = ', '.join(['%s' for item in values])

		query_stmt = """
			INSERT INTO `{0}` ({1})
			VALUES ({2});
		""".format(
			self.__escape(table_name),
			fields_str,
			values_str_sub
		)

		with self.conn:
			self.cur.execute(query_stmt, tuple(values))
			return self.cur.lastrowid


	def find_by_fields(self, table_name, where_props={}, limit=None):
		"""
		MySQL driver interface method for finding records by conditionals.

		TODO:
			- add AND/OR specification to WHERE clause
			- add conditional type specification to WHERE clause:
				(=, !=, >, <, >=, <=)

		Args:
			table_name (str): Name of MySQL table.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.
			limit (int or None): Positive integer limit for query results list.

		Returns:
			List of dictionaries representing MySQL records (deserialized).

		"""

		query_stmt_components = []

		select_component = 'SELECT * FROM `{}`'.format(
			self.__escape(table_name)
		)
		query_stmt_components.append(select_component)

		where_values = None
		if len(where_props.keys()) > 0:
			where_fields = []
			where_values = []
			for key, val in where_props.items():
				where_fields.append(key)
				where_values.append(val)
			where_component = 'WHERE ' + ' AND '.join([
				'`{}`=%s'.format(self.__escape(field))
				for field in where_fields
			])
			query_stmt_components.append(where_component)
			where_values = tuple(where_values)

		if(limit is not None and int(limit) > 0):
			limit_component = 'LIMIT {}'.format(self.__escape(str(limit)))
			query_stmt_components.append(limit_component)

		query_stmt = ' '.join(query_stmt_components) + ';'

		with self.conn:
			if where_values is not None:
				self.cur.execute(query_stmt, where_values)
			else:
				self.cur.execute(query_stmt)
			return self.cur.fetchall()


	def update_by_fields(self, table_name, value_props={}, where_props={}):
		"""
		MySQL driver interface method for updating records by conditionals.

		TODO:
			- add AND/OR specification to WHERE clause
			- add conditional type specification to WHERE clause:
				(=, !=, >, <, >=, <=)

		Args:
			table_name (str): Name of MySQL table.
			value_props (dict): Dictionary of column update values where
				key=column name and value=column value.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.

		Returns:
			(integer) Number of rows updated.

		"""

		# remove 'id' an 'created_ts' keys from dictionary since they should
		# never be mutated
		if 'id' in value_props:
			value_props.pop('id')
		if self.RECORD_CREATED_TS_COLUMN in value_props:
			value_props.pop(self.RECORD_CREATED_TS_COLUMN)
		# mutate 'updated_ts' column to current time on update
		value_props[self.RECORD_UPDATED_TS_COLUMN] = int(time.time())

		query_stmt_components = []

		update_component = 'UPDATE `{}`'.format(
			self.__escape(table_name)
		)
		query_stmt_components.append(update_component)

		set_values = None
		if len(value_props.keys()) > 0:
			set_fields = []
			set_values = []
			for key, val in value_props.items():
				set_fields.append(key)
				set_values.append(val)
			set_component = 'SET ' + ', '.join([
				'`{}`=%s'.format(self.__escape(field))
				for field in set_fields
			])
			query_stmt_components.append(set_component)
		else:
			raise RuntimeError(
				"argument 'value_props' required with at least one SET item"
			)

		where_values = None
		if len(where_props.keys()) > 0:
			where_fields = []
			where_values = []
			for key, val in where_props.items():
				where_fields.append(key)
				where_values.append(val)
			where_component = 'WHERE ' + ' AND '.join([
				'`{}`=%s'.format(self.__escape(field))
				for field in where_fields
			])
			query_stmt_components.append(where_component)
		else:
			raise RuntimeError(
				"argument 'where_props' required with at least one WHERE " +
				"condition"
			)

		query_stmt = ' '.join(query_stmt_components) + ';'

		with self.conn:
			self.cur.execute(query_stmt, tuple(set_values + where_values))
			return self.cur.rowcount


	def delete_by_fields(self, table_name, where_props={}):
		"""
		MySQL driver interface method for deleting records by conditionals.
		TODO:
			- add AND/OR specification to WHERE clause
			- add conditional type specification to WHERE clause:
				(=, !=, >, <, >=, <=)

		Args:
			table_name (str): Name of MySQL table.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.

		Returns:
			(integer) Number of rows updated.

		"""

		query_stmt_components = []

		delete_component = 'DELETE FROM `{}`'.format(
			self.__escape(table_name)
		)
		query_stmt_components.append(delete_component)

		where_values = None
		if len(where_props.keys()) > 0:
			where_fields = []
			where_values = []
			for key, val in where_props.items():
				where_fields.append(key)
				where_values.append(val)
			where_component = 'WHERE ' + ' AND '.join([
				'`{}`=%s'.format(self.__escape(field))
				for field in where_fields
			])
			query_stmt_components.append(where_component)
		else:
			raise RuntimeError(
				"argument 'where_props' required with at least one WHERE " +
				"condition"
			)

		query_stmt = ' '.join(query_stmt_components) + ';'

		with self.conn:
			self.cur.execute(query_stmt, tuple(where_values))
			return self.cur.rowcount


	########## TABLE UTILITIES ##########

	def create_table(self, table_name, column_props={}):
		ppp('MySqlDriver.create_table not implemented yet...')
		# CREATE TABLE example(
		# 	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
		# 	example_column VARCHAR(255)
		# );
		pass

	def delete_table_contents(self, table_name):
		ppp('MySqlDriver.delete_table_contents not implemented yet...')
		# TRUNCATE TABLE table_name;
		pass

	def delete_table(self, table_name):
		ppp('MySqlDriver.delete_table not implemented yet...')
		# DROP TABLE table_name
		pass

	def describe_table(self, table_name):
		query_stmt = "DESC {};".format(
			self.__escape(table_name)
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


	########## PRIVATE HELPERS ##########

	# escape strings for use in query strings
	def __escape(self, string):
		return mdb.escape_string(string).decode('utf-8')


