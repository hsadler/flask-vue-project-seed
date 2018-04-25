
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
		self.r = redis.StrictRedis(
			host=config.REDIS_HOST,
			port=config.REDIS_PORT,
		)


	########## CRUD INTERFACE METHODS ##########


	def set(self, key, value, ttl=None):
		json_value = json.dumps(value)
		if ttl is not None:
			return self.r.set(key, json_value, ex=ttl)
		else:
			return self.r.set(key, json_value)


	def get(self, key):
		json_value = self.r.get(key)
		if json_value is not None:
			value = json.loads(json_value)
			return value
		else:
			return None


	def delete(self, key):
		return self.r.delete(key)



