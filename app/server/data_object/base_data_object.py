
# Base Data Object

from abc import ABCMeta, abstractmethod


class BaseDataObject(metaclass=ABCMeta):
	"""
	Provides base methods and interface for all proper data objects.
	"""


	def __init__(self, prop_dict, db_driver, cache_driver):
		self.db_driver = db_driver
		self.cache_driver = cache_driver
		self.state = prop_dict


	########## BASE METHODS ##########


	@classmethod
	def create(cls, prop_dict={}, db_driver=None, cache_driver=None):

		db_driver, cache_driver = cls.__get_drivers(db_driver, cache_driver)

		return cls(
			prop_dict=prop_dict,
			db_driver=db_driver,
			cache_driver=cache_driver
		)


	@classmethod
	def find_many(
		cls,
		prop_dict={},
		limit=None,
		db_driver=None,
		cache_driver=None
	):

		db_driver, cache_driver = cls.__get_drivers(db_driver, cache_driver)

		records = db_driver.find_by_fields(
			table_name=cls.TABLE_NAME,
			where_props=prop_dict,
			limit=limit
		)

		instances = [
			cls(
				prop_dict=record,
				db_driver=db_driver,
				cache_driver=cache_driver
			)
			for record in records
		]

		return instances


	@classmethod
	def find_one(cls, prop_dict={}, db_driver=None, cache_driver=None):

		instance_list = cls.find_many(
			prop_dict=prop_dict,
			limit=1,
			db_driver=db_driver,
			cache_driver=cache_driver
		)

		if len(instance_list) > 0:
			return instance_list[0]
		else:
			return None


	def get_prop(self, prop_name):
		return self.state[prop_name]


	def set_prop(self, prop_name, prop_value):
		if prop_name in self.state:
			self.state[prop_name] = prop_value
			return True
		else:
			return False


	def save(self):
		pass


	def delete(self):
		pass


	########## INTERFACE METHODS ##########

	@abstractmethod
	to_dict(self):
	pass


	########## PRIVATE HELPERS ##########


	__get_drivers(db_driver=None, cache_driver=None):

		db_driver = db_driver if db_driver is not None \
		else cls.DEFAULT_DB_DRIVER

		cache_driver = cache_driver if cache_driver is not None \
		else cls.DEFAULT_CACHE_DRIVER

		return db_driver, cache_driver


	__get_prop_names():
		pass





