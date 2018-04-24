
# Redis Cache Driver

import redis
import config.config as config
from data_store.cache_driver.base_cache_driver import BaseCacheDriver
from utils.print import ppp

import time


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


	def set(self, key, value):
		return self.r.set(key, value)


	def get(self, key):
		return self.r.get(key)


	def delete(self, key):
		return self.r.delete(key)



