
# Master Redis Cache Configuration

from data_store.cache_config.redis.redis_config import RedisConfig
import config.config as config


class MasterRedisCache(RedisConfig):
	"""
	Configuration for the master Redis cache.

	"""

	HOST = config.MASTER_REDIS_HOST
	PORT = config.MASTER_REDIS_PORT

