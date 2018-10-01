
import sys
sys.path.append('..')

import config.config as config
from data_object.base_data_object import BaseDataObject
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.cache_driver.redis_driver import RedisDriver
from testie import Testie
from utils.print import ppp


"""
Test Base Data Object.

"""


t = Testie()

mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)

TABLE_NAME = 'test_user'


######## DELETE TEST TABLE ########


drop_table_query = """
	DROP TABLE IF EXISTS {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)


######## CREATE TEST TABLE ########


create_table_query = """
	CREATE TABLE IF NOT EXISTS {0} (
		uuid VARCHAR(32) PRIMARY KEY,
		created_ts INT(11) NOT NULL,
		updated_ts INT(11) NOT NULL,
		name VARCHAR(255),
		age INT(4),
		admin TINYINT(1)
	)
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=create_table_query)
ppp('result of create table query:', query_result)


######## CREATE DATA OBJECT CLASS BASED ON TEST TABLE ########


class TestUserDataObject(BaseDataObject):
	TABLE_NAME = 'test_user'
	DEFAULT_DB_DRIVER_CLASS = MySqlDriver
	DEFAULT_CACHE_DRIVER_CLASS = RedisDriver
	DEFAULT_CACHE_TTL = 1


######## TEST DATA OBJECT CRUD INTERFACE ########


# test 'create' method
user_data = {
	'name': 'Harry',
	'age': 36,
	'admin': True
}
test_user_DO = TestUserDataObject.create(prop_dict=user_data)
ppp("'create' method data object:", test_user_DO.to_dict())
t.should_be_equal(
	expected=user_data,
	actual=test_user_DO.to_dict()['state']
)


# test 'save' method
test_user_DO.save()
ppp("saved data object:", test_user_DO.to_dict())
t.should_be_equal(
	expected=TestUserDataObject,
	actual=type(test_user_DO)
)


# test retrieve single by uuid from 'find_many' method
find_id = test_user_DO.get_prop('uuid')
found_test_user_DOs = TestUserDataObject.find_many(
	prop_dict={ 'uuid': find_id }
)
found_test_user_DO = found_test_user_DOs[0]
ppp("'find_many' method data object:", found_test_user_DO.to_dict())
t.should_be_equal(
	expected=test_user_DO.to_dict(),
	actual=found_test_user_DO.to_dict()
)

# test retrieve multiple by non-uuid prop from 'find_many' method
second_test_user_DO = TestUserDataObject.create(prop_dict=user_data)
second_test_user_DO.save()
found_test_user_DOs = TestUserDataObject.find_many(
	prop_dict={ 'age': user_data['age'] }
)
ppp(
	"'find_many' method data objects:",
	[ x.to_dict() for x in found_test_user_DOs ]
)
t.should_be_equal(
	expected=True,
	actual=len(found_test_user_DOs) > 1
)


# test retrieve by uuid 'find_one' method
found_test_user_DO = TestUserDataObject.find_one(
	prop_dict={ 'uuid': test_user_DO.get_prop('uuid') }
)
ppp("'find_one' method data object (by uuid):", found_test_user_DO.to_dict())
t.should_be_equal(
	expected=test_user_DO.to_dict(),
	actual=found_test_user_DO.to_dict()
)

# test retrieve by non-uuid prop 'find_one' method
user_data = {
	'name': 'Jimbo',
	'age': 40,
	'admin': False
}
test_user_DO = TestUserDataObject.create(prop_dict=user_data)
test_user_DO.save()
found_test_user_DO = TestUserDataObject.find_one(
	prop_dict={ 'name': test_user_DO.get_prop('name') }
)
ppp(
	"'find_one' method data object (by non-uuid prop):",
	found_test_user_DO.to_dict()
)
t.should_be_equal(
	expected=test_user_DO.to_dict(),
	actual=found_test_user_DO.to_dict()
)


user_data = {
	'name': 'Ferd',
	'age': 32,
	'admin': True
}
test_user_DO_1 = TestUserDataObject.create(prop_dict=user_data)
test_user_DO_1.save()
user_data = {
	'name': 'Sam',
	'age': 55,
	'admin': True
}
test_user_DO_2 = TestUserDataObject.create(prop_dict=user_data)
test_user_DO_2.save()


# test 'find_by_uuids' method
found_user_DOs = TestUserDataObject.find_by_uuids(
	uuids=[ x.get_prop('uuid') for x in [test_user_DO_1, test_user_DO_2] ]
)
ppp(
	"'find_by_uuids' method found user data objects:",
	[ x.to_dict() for x in found_user_DOs.values() ]
)
t.should_be_equal(
	expected=[str, str],
	actual=[ type(x) for x in found_user_DOs.keys() ]
)
t.should_be_equal(
	expected=2,
	actual=len(found_user_DOs)
)
t.should_be_equal(
	expected=[TestUserDataObject, TestUserDataObject],
	actual=[ type(x) for x in found_user_DOs.values() ]
)


# test 'find_by_uuid' method
# @classmethod
# def find_by_uuid(
# 	cls,
# 	uuid,
# 	db_driver_class=None,
# 	cache_driver_class=None,
# 	cache_ttl=None
# ):


# test 'delete' method
delete_res = found_test_user_DO.delete()
ppp("'delete' res:", delete_res)
t.should_be_equal(
	expected=bool,
	actual=type(delete_res)
)


########## TEST DATA OBJECT DATA ACCESS INTERFACE ##########


user_data = {
	'name': 'Frank',
	'age': 32,
	'admin': 1
}
test_user_DO = TestUserDataObject.create(prop_dict=user_data)
test_user_DO.save()


# test 'get_prop' method
test_user_name = test_user_DO.get_prop(prop_name='name')
ppp("'get_prop' method name property:", test_user_name)
t.should_be_equal(
	expected=user_data['name'],
	actual=test_user_name
)


# test 'set_prop' method
new_age = 101
set_prop_res = test_user_DO.set_prop(prop_name='age', prop_value=new_age)
ppp("'set_prop' res:", set_prop_res)
ppp("test user data object after 'set_prop':", test_user_DO.to_dict())
t.should_be_equal(
	expected=new_age,
	actual=test_user_DO.get_prop(prop_name='age')
)

# test 'get_metadata' method
test_user_created_ts = test_user_DO.get_metadata(
	TestUserDataObject.CREATED_TS_METADATA
)
ppp("'get_metadata' method 'created_ts' property:", test_user_created_ts)
t.should_be_equal(
	expected=type(test_user_created_ts),
	actual=int
)


# test 'set_metadata' method (metadata is managed automatically within the
# dataobject so this method shouldn't ever need to be used)
new_updated_ts = 666
set_metadata_res = test_user_DO.set_metadata(
	metadata_name=TestUserDataObject.UPDATED_TS_METADATA,
	metadata_value=new_updated_ts
)
ppp("'set_metadata' res:", set_metadata_res)
ppp("test user data object after 'set_metadata':", test_user_DO.to_dict())
t.should_be_equal(
	expected=new_updated_ts,
	actual=test_user_DO.get_metadata(
		metadata_name=TestUserDataObject.UPDATED_TS_METADATA
	)
)


########## TEST DATA OBJECT SERIALIZATION, DATABASE, CACHE INTERFACE ##########


# @classmethod
# def load_database_records(
# 	cls,
# 	records,
# 	db_driver_class,
# 	cache_driver_class,
# 	records_are_new=False
# ):


# @classmethod
# def get_drivers(cls, db_driver_class=None, cache_driver_class=None):


# @classmethod
# def load_from_database_by_uuids(
# 	cls,
# 	uuids,
# 	db_driver_class,
# 	cache_driver_class
# ):


# @classmethod
# def load_from_database_by_uuid(
# 	cls,
# 	uuid,
# 	db_driver_class,
# 	cache_driver_class
# ):


# @classmethod
# def construct_cache_key(cls, uuid):


# def set_to_cache(self, ttl=None):


# @classmethod
# def set_batch_to_cache(
# 	cls,
# 	dataobjects,
# 	db_driver_class,
# 	cache_driver_class,
# 	ttl=None,
# ):


# def delete_from_cache(self):


# @classmethod
# def delete_batch_from_cache(cls, dataobjects=[]):


# @classmethod
# def load_from_cache_by_uuids(
# 	cls,
# 	uuids,
# 	db_driver_class,
# 	cache_driver_class
# ):


# @classmethod
# def load_from_cache_by_uuid(cls, uuid, db_driver_class, cache_driver_class):


########## TEST DATA OBJECT UTILITY INTERFACE ##########


# def to_dict(self):


# def to_json(self, pretty=False):


######## DELETE TEST TABLE ########


drop_table_query = """
	DROP TABLE {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)


t.print_report()

