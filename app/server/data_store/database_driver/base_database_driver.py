
# Base Database Driver

from abc import ABCMeta, abstractmethod


class BaseDatabaseDriver(metaclass=ABCMeta):
	"""
	Provides interface for all proper database drivers.

	"""


	@abstractmethod
	def __init__(self, db_config):
		pass


	########## CRUD INTERFACE METHODS ##########

	@abstractmethod
	def insert(self, table_name, value_props={}):
		pass

	@abstractmethod
	def find_by_uuid(self, table_name, uuid):
		pass

	@abstractmethod
	def find_by_fields(self, table_name, where_props={}, limit=None):
		pass

	@abstractmethod
	def update_by_uuid(self, table_name, uuid, value_props={}):
		pass

	@abstractmethod
	def update_by_fields(self, table_name, value_props={}, where_props={}):
		pass

	@abstractmethod
	def delete_by_uuid(self, table_name, uuid):
		pass

	@abstractmethod
	def delete_by_fields(self, table_name, where_props={}):
		pass


	########## TABLE UTILITIES ##########

	@abstractmethod
	def describe_table(self, table_name):
		pass

	@abstractmethod
	def get_table_field_names(self, table_name):
		pass


	########## DATABASE UTILITIES ##########

	@abstractmethod
	def get_database_size(self):
		pass

