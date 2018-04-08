
# MySQL Database Driver

import MySQLdb as mdb
from utils.print import ppp


class MySqlDriver():


	def __init__(self, database_name):
		self.database_name = self.__escape(database_name)
		self.conn = mdb.connect(
			host='mysql', # replace with config val
			user='root', # replace with config val
			passwd='password', # replace with config val
			db=database_name
		)
		self.cur = self.conn.cursor(mdb.cursors.DictCursor)
		self.conn.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')


	########## CRUD INTERFACE METHODS ##########

	def insert(self, table_name, value_props={}):

		res = {}

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
			try:
				self.cur.execute(query_stmt, tuple(values))
				res['success'] = 1
				res['record_id'] = self.cur.lastrowid
				return res
			except Exception as e:
				res['success'] = 0
				res['exception'] = e
				res['query'] = self.cur._last_executed
				return res

	def find_by_fields(self, table_name, where_props={}):
		ppp('MySqlDriver.find_by_fields not implemented yet...')
		# ex:
		# SELECT field1, field2,...fieldN
		# FROM table_name1, table_name2...
		# [WHERE Clause]
		# [OFFSET M ][LIMIT N]
		pass

	def update_by_fields(self, table_name, value_props={}, where_props={}):
		ppp('MySqlDriver.update_by_fields not implemented yet...')
		# ex:
		# UPDATE table_name SET field1 = new-value1, field2 = new-value2
		# [WHERE Clause]
		pass

	def delete_by_fields(self, table_name, where_props={}):
		ppp('MySqlDriver.delete_by_fields not implemented yet...')
		# ex:
		# DELETE FROM table_name [WHERE Clause]
		pass


	########## DATABASE UTILITIES ##########

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

	def describe_table(self, table_name):
		query_stmt = "DESC {};".format(
			self.__escape(table_name)
		)
		with self.conn:
			self.cur.execute(query_stmt)
		return self.cur.fetchall()


	########## HELPERS ##########

	# escape strings for use in query strings
	def __escape(self, string):
		return mdb.escape_string(string).decode('utf-8')


