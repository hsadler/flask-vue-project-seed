
# Redis Config

import redis


class RedisConfig():
	"""
	Singleton base class for all Redis cache configurations.

	"""

	instance = None


	def __init__(self, host, port):
		self.r = redis.StrictRedis(
			host=host,
			port=port
		)


	@classmethod
	def get_instance(cls):
		if cls.instance is None:
			cls.instance = cls(
				host=cls.HOST,
				port=cls.PORT
			)
			return cls.instance
		else:
			return cls.instance

