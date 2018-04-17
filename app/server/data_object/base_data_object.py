
# Base Data Object

from abc import ABCMeta, abstractmethod


class BaseDataObject(metaclass=ABCMeta):
	"""
	Provides base methods and interface for all proper data objects.
	"""


	def __init__(self, prop_dict={}):
		pass


	########## BASE METHODS ##########

	@classmethod
	def create(cls, prop_dict={}):
		pass

	@classmethod
	def find_many(cls, prop_dict={}, limit=None):
		pass

	@classmethod
	def find_one(cls, prop_dict={}):
		pass

	def get_prop(self, prop_name):
		pass

	def set_prop(self, prop_name, prop_value):
		pass

	def save(self):
		pass

	def delete(self):
		pass


	########## INTERFACE METHODS ##########

	@abstractmethod
	to_dict(self):
	pass


	########## PRIVATE HELPERS ##########

	__get_prop_names():
		pass





