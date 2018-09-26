
# Redis Cache Driver

import redis
import simplejson as json

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


	def batch_set(self, items={}, ttl=None):
		"""
		Redis driver interface method for batch setting values with keys and a
		time-to-live.

		Args:
			items (dict): Cache keys and values to set.
			ttl (int): Cached item time-to-live in seconds.

		Returns:
			(dict) Cache key -> bool set status for each item in batch.

		"""

		pipe = self.r.pipeline()
		keys = []
		values = []
		result = {}

		for key, val in items.items():
			keys.append(key)
			values.append(val)

		for i, key in enumerate(keys):
			value = values[i]
			if type(key) is not str or value is None:
				result[key] = False
				continue
			json_value = json.dumps(value)
			if ttl is not None:
				pipe.set(key, json_value, ex=ttl)
			else:
				pipe.set(key, json_value)

		set_statuses = pipe.execute()

		for i, set_status in enumerate(set_statuses):
			result[keys[i]] = set_status

		return result


	def set(self, key, value, ttl=None):
		"""
		Redis driver interface method for setting a value with a key and a
		time-to-live.

		Args:
			key (str): Cache key.
			value (mixed): Python data structure to save to cache.
			ttl (int): Cached item time-to-live in seconds.

		Returns:
			(bool) Successful cache set.

		"""

		if type(key) is not str or value is None:
			return False

		json_value = json.dumps(value)
		if ttl is not None:
			return self.r.set(key, json_value, ex=ttl)
		else:
			return self.r.set(key, json_value)


	def batch_get(self, keys=[]):
		"""
		Redis driver interface method for getting cached values by keys in
		batch.

		Args:
			keys (list): List of cache key strings.

		Returns:
			(dict) Cache key -> cache value (or None if not found)

		"""

		pipe = self.r.pipeline()

		for key in keys:
			pipe.get(key)

		redis_response = pipe.execute()

		cached_values = [
			json.loads(x) if x is not None else x
			for x in redis_response
		]

		result = {}
		for i, value in enumerate(cached_values):
			result[keys[i]] = value

		return result


	def get(self, key):
		"""
		Redis driver interface method for getting a cached value by key.

		Args:
			key (str): Cache key.

		Returns:
			(mixed) Cached python data structure value or None if not found.

		"""

		json_value = self.r.get(key)
		if json_value is not None:
			value = json.loads(json_value)
			return value
		else:
			return None


	def batch_delete(self, keys=[]):
		"""
		Redis driver interface method for deleting cached items by keys for a
		batch.

		Args:
			keys (list): List of cache key strings.

		Returns:
			(dict) Cache key -> int delete status for each item in batch.

		"""

		pipe = self.r.pipeline()

		for key in keys:
			pipe.delete(key)

		delete_statuses = pipe.execute()

		result = {}
		for i, delete_status in enumerate(delete_statuses):
			result[keys[i]] = delete_status

		return result


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
			(list) List of cache key strings.

		"""

		return [ str(x, 'utf-8') for x in self.r.keys() ]



