
# Redis Cache Driver

import redis
import json

import config.config as config
from data_store.cache_driver.base_cache_driver import BaseCacheDriver
from utils.print import ppp


class RedisDriver(BaseCacheDriver):
	"""
	Redis cache driver which implements CRUD and utility public methods.

	"""


	def __init__(self):
		"""
		Redis driver instance constructor. Configures the Redis connection with
		host and port.

		"""

		self.r = redis.StrictRedis(
			host=config.REDIS_HOST,
			port=config.REDIS_PORT,
		)


	########## CRUD INTERFACE METHODS ##########


	def set(self, key, value, ttl=None):
		"""
		Redis driver interface method for setting values with key and
		time-to-live.

		Args:
			key (str): Cache key.
			value (mixed): Python data structure to save to cache.
			ttl (int): Cached item time-to-live in seconds.

		Returns:
			(bool) Successful cache set.

		"""

		json_value = json.dumps(value)
		if ttl is not None:
			return self.r.set(key, json_value, ex=ttl)
		else:
			return self.r.set(key, json_value)


	def get(self, key):
		"""
		Redis driver interface method for getting cached values by key.

		Args:
			key (str): Cache key.

		Returns:
			(mixed) Cached python data structre value.

		"""

		json_value = self.r.get(key)
		if json_value is not None:
			value = json.loads(json_value)
			return value
		else:
			return None


	def delete(self, key):
		"""
		Redis driver interface method for deleting cached items by key.

		Args:
			key (str): Cache key.

		Returns:
			(int) Successful cache delete.

		"""

		return self.r.delete(key)


	########## REDIS SPECIFIC METHODS ##########


	def get_all_keys(self):
		"""
		Get a list of all currently set Redis cache keys.

		Returns:
			(list) List of strings.

		"""

		return [ str(x, 'utf-8') for x in self.r.keys() ]



