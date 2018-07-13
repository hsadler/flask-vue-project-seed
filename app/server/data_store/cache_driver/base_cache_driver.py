
# Base Cache Driver

from abc import ABCMeta, abstractmethod


class BaseCacheDriver(metaclass=ABCMeta):
	"""
	Provides interface for all proper cache drivers.
	"""


	@abstractmethod
	def __init__(self):
		pass


	########## CRUD INTERFACE METHODS ##########

	@abstractmethod
	def set_batch(self, items={}, ttl=None):
		pass

	@abstractmethod
	def set_single(self, key, value, ttl=None):
		pass

	# @abstractmethod
	# def get_batch(self, keys):
	# 	pass

	@abstractmethod
	def get_single(self, key):
		pass

	# @abstractmethod
	# def delete_batch(self, keys):
	# 	pass

	@abstractmethod
	def delete_single(self, key):
		pass

