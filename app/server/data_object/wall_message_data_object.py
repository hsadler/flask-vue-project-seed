
# Wall Message Data Object

from data_object.base_data_object import BaseDataObject
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.cache_driver.redis_driver import RedisDriver
from data_store.database_config.mysql.master_mysql_db import MasterMySqlDB
from data_store.cache_config.redis.master_redis_cache import MasterRedisCache


class WallMessageDataObject(BaseDataObject):
	"""
	Wall Message Data Object

	"""


	TABLE_NAME = 'wall_message'
	DEFAULT_DB_DRIVER = MySqlDriver(db_config=MasterMySqlDB.get_instance())
	DEFAULT_CACHE_DRIVER = RedisDriver(
		cache_config=MasterRedisCache.get_instance()
	)
	DEFAULT_CACHE_TTL = 30

