
# MySQL Database Driver

import MySQLdb as mdb


class MySQLdbDriver():


	def __init__(self, database_name):
		self.database_name = database_name
		self.connection = mdb.connect(
			host='mysql', # replace with config val
			user='root', # replace with config val
			passwd='password', # replace with config val
			db=database_name
		)
		self.cur = self.connection.cursor(mdb.cursors.DictCursor)
		self.connection.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')


	def get_size(self, table_name):
		with self.connection:
			self.cur.execute(
				"""SELECT table_name AS "Table",
				ROUND(((data_length + index_length) / 1024 / 1024), 2)
				AS "Size (MB)"
				FROM information_schema.TABLES
				WHERE table_schema = %s
				ORDER BY (data_length + index_length) DESC;""",
				(table_name,)
			)
		return self.cur.fetchall()
