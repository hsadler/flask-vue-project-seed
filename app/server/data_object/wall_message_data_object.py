
# Wall Message Data Object

from data_object.base_data_object import BaseDataObject
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.cache_driver.redis_driver import RedisDriver


class WallMessageDataObject(BaseDataObject):
	"""
	Wall Message Data Object

	"""


	TABLE_NAME = 'wall_message'
	DEFAULT_DB_DRIVER_CLASS = MySqlDriver
	DEFAULT_CACHE_DRIVER_CLASS = RedisDriver
	DEFAULT_CACHE_TTL = 30

