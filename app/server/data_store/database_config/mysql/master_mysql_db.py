
# Master MySQL Database Configuration

from data_store.database_config.mysql.mysql_config import MySqlConfig
import config.config as config


class MasterMySqlDB(MySqlConfig):
	"""
	Provides interface for all MySQL database configurations.

	"""

	HOST = config.MASTER_MYSQL_HOST
	USER = config.MASTER_MYSQL_USER
	PASSWORD = config.MASTER_MYSQL_PASSWORD
	DATABASE = config.MASTER_MYSQL_DB_NAME

