
import time
import sys
sys.path.append('..')

from data_object.example_data_object import ExampleDataObject
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.cache_driver.redis_driver import RedisDriver
from utils.print import ppp


######## TEST DATA OBJECT INTERFACE ########


# test create
created_example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'hello world!' }
)
ppp(['created example data object: ', created_example_DO.to_dict()])


# test find_many
found_example_DOs = ExampleDataObject.find_many(
	prop_dict={ 'field': 'hello world!' },
	limit=3
)
ppp('found example data objects:')
for ex_DO in found_example_DOs:
	ppp(ex_DO.to_dict())


# test find_one
found_example_DO = ExampleDataObject.find_one(
	prop_dict={'id': 1}
)
ppp(['found one example data object: ', found_example_DO.to_dict()])


# test get_prop
property_name = 'field'
property_value = found_example_DO.get_prop(prop_name=property_name)
ppp('retrieved property "key"->{0}, "value"->{1}'.format(
	property_name,
	property_value
))


# test set_prop
property_name = 'field'
property_value = 'hi there again!'
found_example_DO.set_prop(
	prop_name=property_name,
	prop_value=property_value
)
ppp([
	'set property "key"->{0}, "value"->{1} for example data object:'.format(
		property_name,
		property_value
	),
	found_example_DO.to_dict()
])


# test save
saved_example_DO = found_example_DO.save()
ppp(['saved example data object:', saved_example_DO.to_dict()])


# test delete
to_delete_example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'delete me...' }
)
to_delete_example_DO = to_delete_example_DO.save()
ppp(['data object to delete:', to_delete_example_DO.to_dict()])
record_was_deleted = to_delete_example_DO.delete()
ppp('record was deleted: {0}'.format(record_was_deleted))


# test caching
example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'i am going to be cached' }
)
saved_and_cached_example_DO = example_DO.save(cache_ttl=1)

from_cache_example_DO = ExampleDataObject.load_from_cache(
	id=saved_and_cached_example_DO.get_prop('id'),
	db_driver_class=MySqlDriver,
	cache_driver_class=RedisDriver
)
ppp(['this should exist in the Redis cache:', from_cache_example_DO])

time.sleep(2)
from_cache_example_DO = ExampleDataObject.load_from_cache(
	id=saved_and_cached_example_DO.get_prop('id'),
	db_driver_class=MySqlDriver,
	cache_driver_class=RedisDriver
)
ppp(['this should NOT exist in the Redis cache:', from_cache_example_DO])



