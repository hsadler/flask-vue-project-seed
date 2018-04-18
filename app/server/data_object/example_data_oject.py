
# Example Data Object

from dataobject.base_data_object import BaseDataObject
from data_store.database_driver.mysql_driver import MySqlDriver


class ExampleDataObject(BaseDataObject):
	"""
	Example Data Object
	"""


	TABLE_NAME = 'example'
	DEFAULT_DB_DRIVER = MySqlDriver()
	DEFAULT_CACHE_DRIVER = None


	# Subclass specific methods go here...

