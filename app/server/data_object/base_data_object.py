
# Base Data Object

import sys
import config.config as config

from abc import ABCMeta, abstractmethod
import json


class BaseDataObject(metaclass=ABCMeta):
	"""
	Provides base methods and interface for all proper data objects.

	TODO:
		X test
		X add caching
		- write docstrings for all methods
	"""


	def __init__(self, prop_dict, db_driver_class, cache_driver_class):
		self.db_driver_class = db_driver_class
		self.cache_driver_class = cache_driver_class
		db_driver, cache_driver = self.__get_drivers(
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)
		self.db_driver = db_driver
		self.cache_driver = cache_driver
		self.state = prop_dict


	########## BASE METHODS ##########


	@classmethod
	def create(
		cls,
		prop_dict={},
		db_driver_class=None,
		cache_driver_class=None
	):

		return cls(
			prop_dict=prop_dict,
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)


	@classmethod
	def find_many(
		cls,
		prop_dict={},
		limit=None,
		db_driver_class=None,
		cache_driver_class=None
	):
		"""
		Note: There is NO CACHING for this 'batch find' method
		"""

		db_driver, cache_driver = cls.__get_drivers(
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)

		records = db_driver.find_by_fields(
			table_name=cls.TABLE_NAME,
			where_props=prop_dict,
			limit=limit
		)

		instances = [
			cls(
				prop_dict=record,
				db_driver_class=db_driver_class,
				cache_driver_class=cache_driver_class
			)
			for record in records
		]

		return instances


	@classmethod
	def find_one(
		cls,
		prop_dict={},
		db_driver_class=None,
		cache_driver_class=None
	):

		# only check cache if finding solely by id
		find_props = list(prop_dict.keys())
		if len(find_props) == 1 and find_props[0] == 'id':
			instance = cls.__load_from_cache(
				id=prop_dict['id'],
				db_driver_class=db_driver_class,
				cache_driver_class=cache_driver_class
			)
			if instance is not None:
				instance.__set_to_cache()
				return instance

		instance_list = cls.find_many(
			prop_dict=prop_dict,
			limit=1,
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
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


	def save(self, cache_ttl=None):

		result = None

		# existing record
		if 'id' in self.state:
			record_update_count = self.db_driver.update_by_fields(
				table_name=self.TABLE_NAME,
				value_props=self.state,
				where_props={
					'id': self.get_prop('id')
				}
			)
			result = self if record_update_count == 1 else None
		# new record
		else:
			new_record_id = self.db_driver.insert(
				table_name=self.TABLE_NAME,
				value_props=self.state
			)
			if new_record_id > 0:
				result = self.find_one(prop_dict={ 'id': new_record_id })

		if result is not None:
			result.__set_to_cache()

		return result


	def delete(self):
		record_delete_count = self.db_driver.delete_by_fields(
			table_name=self.TABLE_NAME,
			where_props={
				'id': self.get_prop('id')
			}
		)
		if record_delete_count > 0:
			self.__delete_from_cache()
			return True
		else:
			return False


	########## UTILITY METHODS ##########


	def to_dict(self):
		return self.state


	def to_json(self, pretty=False):
		if pretty:
			return json.dumps(self.state, sort_keys=True, indent=2)
		else:
			return json.dumps(self.state)


	########## INTERFACE METHODS ##########


	# ...


	########## PRIVATE HELPERS ##########


	@classmethod
	def __get_drivers(cls, db_driver_class=None, cache_driver_class=None):

		db_driver_class = db_driver_class \
		if db_driver_class is not None \
		else cls.DEFAULT_DB_DRIVER_CLASS

		cache_driver_class = cache_driver_class \
		if cache_driver_class is not None \
		else cls.DEFAULT_CACHE_DRIVER_CLASS

		db_driver = None
		cache_driver = None

		if db_driver_class is not None:
			db_driver = db_driver_class(
				database_name=config.MYSQL_DB_NAME
			)

		if cache_driver_class is not None:
			cache_driver = cache_driver_class()

		return db_driver, cache_driver


	def __get_prop_names(self):
		return self.db_driver.get_table_field_names(self.TABLE_NAME)


	@classmethod
	def __construct_cache_key(cls, id):
		cache_key = '{0}_id={1}'.format(
			cls.TABLE_NAME,
			id
		)
		return cache_key


	def __set_to_cache(self, ttl=None):
		cache_key = self.__construct_cache_key(id=self.get_prop('id'))
		cache_value = self.to_dict()
		ttl = ttl if ttl is not None else self.DEFAULT_CACHE_TTL
		self.cache_driver.set(
			key=cache_key,
			value=cache_value,
			ttl=ttl
		)


	@classmethod
	def __load_from_cache(cls, id, db_driver_class, cache_driver_class):
		db_driver, cache_driver = cls.__get_drivers(
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)
		cache_key = cls.__construct_cache_key(id=id)
		cached_value = cache_driver.get(cache_key)
		if cached_value is not None:
			instance = cls(
				prop_dict=cached_value,
				db_driver_class=db_driver_class,
				cache_driver_class=cache_driver_class
			)
			return instance
		else:
			return None


	def __delete_from_cache(self):
		cache_key = self.__construct_cache_key(id=self.get_prop('id'))
		self.cache_driver.delete(cache_key)




