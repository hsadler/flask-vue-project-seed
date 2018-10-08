
# Master MySQL Database Configuration

import config.config as config


class MasterMySqlDB(BaseMySqlConfig):
	"""
	Provides interface for all MySQL database configurations.

	"""

	HOST = config.MASTER_MYSQL_HOST
	USER = config.MASTER_MYSQL_USER
	PASSWORD = config.MASTER_MYSQL_PASSWORD
	DATABASE = config.MASTER_MYSQL_DB_NAME

