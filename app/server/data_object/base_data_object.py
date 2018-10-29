
# Base Data Object

import sys
import uuid
import simplejson as json
import config.config as config
from abc import ABCMeta, abstractmethod

from utils.print import ppp


class BaseDataObject(metaclass=ABCMeta):
	"""
	Provides base methods and interface for all proper data objects.

	TODO:
		- add and update docstrings
		- asses types of caching currently implemented and research
			alternatives
		- better management of attribute types (int, str, bool, etc.)

	"""


	# attributes require by subclasses (not used, for documentation only)
	REQUIRED_SUBCLASS_ATTRIBUTES = [
		'TABLE_NAME',
		'DEFAULT_DB_DRIVER',
		'DEFAULT_CACHE_DRIVER',
		'DEFAULT_CACHE_TTL'
	]

	# properties
	UUID_PROPERTY = 'uuid'

	# metadata
	CREATED_TS_METADATA = 'created_ts'
	UPDATED_TS_METADATA = 'updated_ts'
	METADATA_FIELDS = [
		CREATED_TS_METADATA,
		UPDATED_TS_METADATA
	]


	def __init__(
		self,
		prop_dict,
		metadata_dict={},
		new_record=True,
		db_driver=None,
		cache_driver=None
	):
		"""
		Data object instance constructor. Configures the database driver, cache
		driver, properties, and metadata.

		NOTE: Should not be used in the wild. Use classmethod 'create' instead.

		Args:
			prop_dict (dict): Dictionary representing dataobject properties.
			metadata_dict (dict): Dictionary representing dataobject metadata.
			new_record (bool): Whether or not dataobject is a new DB record.
			db_driver (object): Database driver.
			cache_driver (object): Cache driver.

		"""

		# set properties
		self.properties = prop_dict

		# set metadata initial values
		self.metadata = {
			self.CREATED_TS_METADATA: None,
			self.UPDATED_TS_METADATA: None
		}

		# replace metadata initial values with passed values
		for key, val in metadata_dict.items():
			if key in self.METADATA_FIELDS:
				self.metadata[key] = val

		# set new_record attribute
		self.new_record = new_record

		# set database driver and cache driver
		self.db_driver, self.cache_driver = self.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)


	########## CRUD PUBLIC METHODS ##########


	@classmethod
	def create(
		cls,
		prop_dict={},
		db_driver=None,
		cache_driver=None
	):
		"""
		Data object creation method. NOTE: Does not save to data store.

		Args:
			prop_dict (dict): Dictionary representing data object properties.
			db_driver (object): Database driver.
			cache_driver (object): Cache driver.

		Returns:
			(object) Data object instance.

		"""

		# set uuid upon dataobject creation
		prop_dict[cls.UUID_PROPERTY] = uuid.uuid4().hex

		# use the constructor to set properties, DB driver and cache driver
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
		cache_driver=None,
		cache_ttl=None
	):
		"""
		Data object database search method. Search for multiple records matching
		all properties in the prop_dict dictionary.

		Args:
			prop_dict (dict): Dictionary of propery name to values.
			limit (int): Limit lenth of returned data object list.
			db_driver (object): Database driver.
			cache_driver (object): Cache driver.
			cache_ttl (int): Cache time-to-live in seconds.

		Returns:
			(list) List of data object instances.

		"""

		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)

		# only check cache if finding solely by single uuid
		find_props = list(prop_dict.keys())
		if (
			len(find_props) == 1 and
			find_props[0] == cls.UUID_PROPERTY and
			type(prop_dict[cls.UUID_PROPERTY]) is str
		):
			instance = cls.load_from_cache_by_uuid(
				uuid=prop_dict[cls.UUID_PROPERTY],
				db_driver=db_driver,
				cache_driver=cache_driver
			)
			if instance is not None:
				return [instance]

		# get records from database
		records = db_driver.find_by_fields(
			table_name=cls.TABLE_NAME,
			where_props=prop_dict,
			limit=limit
		)

		# deserialize records to instances
		instances = cls.load_database_records(
			records=records,
			db_driver=db_driver,
			cache_driver=cache_driver,
			records_are_new=False
		)

		# batch cache database found instances on the way out
		if len(instances) > 0:
			cls.set_batch_to_cache(
				dataobjects=instances,
				db_driver=db_driver,
				cache_driver=cache_driver,
				ttl=cache_ttl
			)

		return instances


	@classmethod
	def find_one(
		cls,
		prop_dict={},
		db_driver=None,
		cache_driver=None,
		cache_ttl=None
	):
		"""
		Data object database search method. Search for single records matching
		all properties in the prop_dict dictionary.

		Args:
			prop_dict (dict): Dictionary of propery name to values.
			db_driver (object): Database driver.
			cache_driver (object): Cache driver.
			cache_ttl (int): Cache time-to-live in seconds.

		Returns:
			(object) Data object instance.

		"""

		instance_list = cls.find_many(
			prop_dict=prop_dict,
			limit=1,
			db_driver=db_driver,
			cache_driver=cache_driver,
			cache_ttl=cache_ttl
		)

		if len(instance_list) > 0:
			return instance_list[0]
		else:
			return None


	@classmethod
	def find_by_uuids(
		cls,
		uuids=[],
		db_driver=None,
		cache_driver=None,
		cache_ttl=None
	):

		# get drivers
		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)

		# batch query cache
		instances_dict = cls.load_from_cache_by_uuids(
			uuids=uuids,
			db_driver=db_driver,
			cache_driver=cache_driver
		)

		# get keys not found in cache
		uuids_not_found_in_cache = [
			key for key, val in instances_dict.items()
			if val is None
		]

		# for those not found in the cache, batch query database
		if len(uuids_not_found_in_cache) > 0:
			uuids_to_instances = cls.load_from_database_by_uuids(
				uuids=uuids_not_found_in_cache,
				db_driver=db_driver,
				cache_driver=cache_driver
			)
			# add found database record instances to the aggregate
			for key, val in uuids_to_instances.items():
				instances_dict[key] = val
			# batch set to cache only the instances which came from the DB call
			instances_to_be_cached = [
				inst for inst
				in uuids_to_instances.values()
				if inst is not None
			]
			cls.set_batch_to_cache(
				dataobjects=instances_to_be_cached,
				db_driver=db_driver,
				cache_driver=cache_driver,
				ttl=cache_ttl
			)

		# return the aggregated cache found and database found instances in a
		# uuid->instance dictionary
		return instances_dict


	@classmethod
	def find_by_uuid(
		cls,
		uuid,
		db_driver=None,
		cache_driver=None,
		cache_ttl=None
	):
		prop_dict = {
			cls.UUID_PROPERTY: uuid
		}
		return cls.find_one(
			prop_dict=prop_dict,
			db_driver=db_driver,
			cache_driver=cache_driver,
			cache_ttl=cache_ttl
		)


	def save(self, cache_ttl=None):
		"""
		Data object database save method.

		Args:
			cache_ttl (int): Cache time-to-live in seconds.

		Returns:
			(bool) Database upsert success.

		"""

		# serialize
		serialized_record = self.__serialize_instance_for_database(
			instance=self
		)

		# upsert database record
		upsert_success = False
		if self.new_record:
			# insert record in database
			insert_res = self.db_driver.insert(
				table_name=self.TABLE_NAME,
				value_props=serialized_record
			)
			# update instance properties and metadata
			# (using record as source of truth)
			if insert_res is not None:
				for m_field in self.METADATA_FIELDS:
					self.set_metadata(
						metadata_name=m_field,
						metadata_value=insert_res[m_field]
					)
					del insert_res[m_field]
				for prop_key, prop_val in insert_res.items():
					self.set_prop(
						prop_name=prop_key,
						prop_value=prop_val
					)
				upsert_success = True
		else:
			# update record in database
			update_res = self.db_driver.update_by_uuid(
				table_name=self.TABLE_NAME,
				uuid=self.get_prop(self.UUID_PROPERTY),
				value_props=serialized_record
			)
			# on success, update instance metadata
			if update_res['rows_affected'] == 1:
				self.set_metadata(
					metadata_name=self.UPDATED_TS_METADATA,
					metadata_value=update_res[self.UPDATED_TS_METADATA]
				)
				upsert_success = True

		# cache upserted record and set 'new_record' to False if upsert was
		# successful
		if upsert_success:
			self.new_record = False
			self.set_to_cache(ttl=cache_ttl)

		return upsert_success


	def delete(self):
		"""
		Data object database delete method.

		Returns:
			(bool) Database delete success.

		"""

		record_delete_count = self.db_driver.delete_by_uuid(
			table_name=self.TABLE_NAME,
			uuid=self.get_prop(self.UUID_PROPERTY)
		)
		if record_delete_count > 0:
			self.delete_from_cache()
			return True
		else:
			return False


	########## DATA ACCESS PUBLIC METHODS ##########


	def get_prop(self, prop_name):
		"""
		Data object property getter method. Fails hard on key error.

		Args:
			prop_name (str): Name of property.

		Returns:
			(mixed) Data object property.

		"""

		return self.properties[prop_name]


	def set_prop(self, prop_name, prop_value):
		"""
		Data object property setter method.

		Args:
			prop_name (str): Name of property.
			prop_value (mixed): Property value.

		Returns:
			(bool) Property set success.

		"""

		if prop_name in self.properties:
			self.properties[prop_name] = prop_value
			return True
		else:
			return False


	def get_metadata(self, metadata_name):
		"""
		Data object metadata property getter method.

		Args:
			metadata_name (str): Name of metadata property.

		Returns:
			(mixed) Data object metadata property.

		"""

		return self.metadata[metadata_name]


	def set_metadata(self, metadata_name, metadata_value):
		"""
		Data object metadata property setter method.

		Args:
			metadata_name (str): Name of metadata property.
			metadata_value (mixed): metadata property value.

		Returns:
			(bool) metadataerty set success.

		"""

		if metadata_name in self.metadata:
			self.metadata[metadata_name] = metadata_value
			return True
		else:
			return False


	def get_properties(self):
		return self.properties


	def get_metadatas(self):
		return self.metadata


	########## SERIALIZATION, DATABASE, CACHE PUBLIC METHODS ##########


	@classmethod
	def load_database_records(
		cls,
		records,
		db_driver,
		cache_driver,
		records_are_new=False
	):
		instances = []
		for record in records:
			prop_dict = {}
			metadata_dict = {}
			for prop, val in record.items():
				if prop in cls.METADATA_FIELDS:
					metadata_dict[prop] = val
				else:
					prop_dict[prop] = val
			instance = cls(
				prop_dict=prop_dict,
				db_driver=db_driver,
				cache_driver=cache_driver,
				metadata_dict=metadata_dict,
				new_record=records_are_new
			)
			instances.append(instance)
		return instances


	@classmethod
	def get_drivers(cls, db_driver=None, cache_driver=None):
		# return drivers if they exist otherwise, retrieve from defaults set on
		# subclass
		db_driver = (
			db_driver if db_driver is not None
			else cls.DEFAULT_DB_DRIVER
		)
		cache_driver = (
			cache_driver if cache_driver is not None
			else cls.DEFAULT_CACHE_DRIVER
		)
		return db_driver, cache_driver


	@classmethod
	def load_from_database_by_uuids(
		cls,
		uuids,
		db_driver,
		cache_driver
	):

		# get drivers
		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)

		# query for records from the database
		records = db_driver.find_by_fields(
			table_name=cls.TABLE_NAME,
			where_props={
				cls.UUID_PROPERTY: {
					'in': uuids
				}
			},
			limit=None
		)

		# load instances from records
		instances = cls.load_database_records(
			records=records,
			db_driver=db_driver,
			cache_driver=cache_driver,
			records_are_new=False
		)

		# map uuids to instances
		uuids_to_instances = {
			instance.get_prop(cls.UUID_PROPERTY): instance
			for instance in instances
		}

		# fill in records not found with None values
		for uuid in uuids:
			if uuid not in uuids_to_instances:
				uuids_to_instances[uuid] = None

		return uuids_to_instances


	@classmethod
	def load_from_database_by_uuid(
		cls,
		uuid,
		db_driver,
		cache_driver
	):
		uuids_to_instances = cls.load_from_database_by_uuids(
			uuids=[uuid],
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		if uuid in uuids_to_instances:
			return uuids_to_instances[uuid]
		else:
			return None


	@classmethod
	def construct_cache_key(cls, uuid):
		cache_key = '{0}_uuid={1}'.format(
			cls.TABLE_NAME,
			uuid
		)
		return cache_key


	def set_to_cache(self, ttl=None):
		cache_key = self.construct_cache_key(
			uuid=self.get_prop(self.UUID_PROPERTY)
		)
		cache_value = self.__serialize_instance_for_cache(instance=self)
		ttl = ttl if ttl is not None else self.DEFAULT_CACHE_TTL
		return self.cache_driver.set(
			key=cache_key,
			value=cache_value,
			ttl=ttl
		)


	@classmethod
	def set_batch_to_cache(
		cls,
		dataobjects,
		db_driver,
		cache_driver,
		ttl=None,
	):
		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		cache_key_to_value = {}
		cache_key_to_uuid = {}
		for DO in dataobjects:
			DO_uuid = DO.get_prop(cls.UUID_PROPERTY)
			cache_key = cls.construct_cache_key(
				uuid=DO_uuid
			)
			cache_value = cls.__serialize_instance_for_cache(instance=DO)
			cache_key_to_value[cache_key] = cache_value
			cache_key_to_uuid[cache_key] = DO_uuid
		ttl = ttl if ttl is not None else cls.DEFAULT_CACHE_TTL
		cache_driver_res = cache_driver.batch_set(
			items=cache_key_to_value,
			ttl=ttl
		)
		uuid_to_cache_status = {}
		for cache_key, status in cache_driver_res.items():
			DO_uuid = cache_key_to_uuid[cache_key]
			uuid_to_cache_status[DO_uuid] = status
		return uuid_to_cache_status


	def delete_from_cache(self):
		cache_key = self.construct_cache_key(
			uuid=self.get_prop(self.UUID_PROPERTY)
		)
		delete_res = self.cache_driver.delete(cache_key)
		return True if delete_res == 1 else False


	@classmethod
	def delete_batch_from_cache(
		cls,
		dataobjects,
		db_driver,
		cache_driver
	):
		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		cache_keys = []
		cache_key_to_uuid = {}
		for DO in dataobjects:
			uuid = DO.get_prop(cls.UUID_PROPERTY)
			cache_key = cls.construct_cache_key(uuid=uuid)
			cache_keys.append(cache_key)
			cache_key_to_uuid[cache_key] = uuid
		batch_delete_res = cache_driver.batch_delete(keys=cache_keys)
		uuids_to_cache_delete_status = {}
		for cache_key, delete_count in batch_delete_res.items():
			uuid = cache_key_to_uuid[cache_key]
			status = True if delete_count == 1 else False
			uuids_to_cache_delete_status[uuid] = status
		return uuids_to_cache_delete_status


	@classmethod
	def load_from_cache_by_uuids(
		cls,
		uuids,
		db_driver,
		cache_driver
	):
		db_driver, cache_driver = cls.get_drivers(
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		cache_keys_to_uuids = {
			cls.construct_cache_key(uuid=uuid): uuid
			for uuid in uuids
		}
		cache_keys = list(cache_keys_to_uuids.keys())
		cache_keys_to_values = cache_driver.batch_get(keys=cache_keys)
		uuids_to_instances = {
			cache_keys_to_uuids[cache_key]: cls.__deserialize_value_from_cache(
				cache_value=cache_value,
				db_driver=db_driver,
				cache_driver=cache_driver
			)
			if cache_value is not None else None
			for cache_key, cache_value
			in cache_keys_to_values.items()
		}
		return uuids_to_instances


	@classmethod
	def load_from_cache_by_uuid(cls, uuid, db_driver, cache_driver):
		uuids_to_instances = cls.load_from_cache_by_uuids(
			uuids=[uuid],
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		return uuids_to_instances[uuid]


	########## UTILITY PUBLIC METHODS ##########


	def to_dict(self):
		"""
		Get data object's properies and metadata in dictionary format.

		Returns:
			(dict) Dictionary representation of data object.

		"""

		return {
			'properties': self.properties,
			'metadata': self.metadata,
			'new_record': self.new_record
		}


	def to_json(self, pretty=False):
		"""
		Get data object's properties and metadata formatted as JSON string.

		Args:
			pretty (bool): Option for getting JSON string in pretty format.

		Returns:
			(str) JSON string.

		"""

		if pretty:
			return json.dumps(self.to_dict(), sort_keys=True, indent=2)
		else:
			return json.dumps(self.to_dict())


	########## PRIVATE METHODS ##########


	@classmethod
	def __serialize_instances_for_database(cls, instances):
		serialized_records = []
		for inst in instances:
			serialized_record = {}
			for m_field, m_value in inst.get_metadatas().items():
				serialized_record[m_field] = m_value
			for s_field, s_value in inst.get_properties().items():
				serialized_record[s_field] = s_value
			serialized_records.append(serialized_record)
		return serialized_records


	@classmethod
	def __serialize_instance_for_database(cls, instance):
		serialized_records = cls.__serialize_instances_for_database(
			instances=[instance]
		)
		if len(serialized_records) > 0:
			return serialized_records[0]
		else:
			return None


	@classmethod
	def __serialize_instances_for_cache(cls, instances):
		serialized = [ inst.to_dict() for inst in instances ]
		return serialized


	@classmethod
	def __serialize_instance_for_cache(cls, instance):
		serialized = cls.__serialize_instances_for_cache(instances=[ instance ])
		if len(serialized) > 0:
			return serialized[0]
		else:
			return None


	@classmethod
	def __deserialize_values_from_cache(
		cls,
		cache_values,
		db_driver,
		cache_driver
	):
		deserialized = [
			cls(
				prop_dict=val['properties'],
				db_driver=db_driver,
				cache_driver=cache_driver,
				metadata_dict=val['metadata'],
				new_record=val['new_record']
			)
			for val in cache_values
		]
		return deserialized


	@classmethod
	def __deserialize_value_from_cache(
		cls,
		cache_value,
		db_driver,
		cache_driver
	):
		values = cls.__deserialize_values_from_cache(
			cache_values=[ cache_value ],
			db_driver=db_driver,
			cache_driver=cache_driver
		)
		if len(values) > 0:
			return values[0]
		else:
			return None


	def __get_database_prop_names(self):
		return self.db_driver.get_table_field_names(self.TABLE_NAME)

