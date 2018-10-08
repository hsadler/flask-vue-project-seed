
# MySQL Config

import MySQLdb as mdb


class MySqlConfig():
	"""
	Singleton base class for all MySQL database configurations.

	"""

	instance = None


	def __init__(self, host, user, password, database):
		self.database_name = self.escape(database)
		self.conn = mdb.connect(
			host=host,
			user=user,
			passwd=password,
			db=database
		)
		self.cur = self.conn.cursor(mdb.cursors.DictCursor)
		self.conn.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')


	@classmethod
	def get_instance(cls):
		if cls.instance is None:
			cls.instance = cls(
				host=cls.HOST,
				user=cls.USER,
				password=cls.PASSWORD,
				database=cls.DATABASE
			)
			return cls.instance
		else:
			return cls.instance

