
import time
import sys
sys.path.append('..')

import config.config as config
from data_store.cache_driver.redis_driver import RedisDriver
from testie import Testie
from utils.print import ppp


t = Testie()

redis_driver = RedisDriver()


######## TEST INTERFACE ########


cache_items = {
	'string': 'my_string',
	'integer': 1234,
	'negative_decimal': -1.234,
	'boolean': True,
	'list': [1, 'cats', False],
	'dictionary': {'one': 1, 'two': 2}
}
cache_ttl = 1

# test single items
for cache_key, cache_value in cache_items.items():

	# test set
	set_response = redis_driver.set(
		key=cache_key,
		value=cache_value,
		ttl=cache_ttl
	)
	ppp('set_response:', set_response)
	t.should_be_equal(expected=True, actual=set_response)

	# test get before expiration
	get_response = redis_driver.get(key=cache_key)
	ppp('get_response:', get_response)
	t.should_be_equal(expected=cache_value, actual=get_response)

	# test get after expiration
	time.sleep(2)
	get_response = redis_driver.get(key=cache_key)
	ppp('get_response:', get_response)
	t.should_be_equal(expected=None, actual=get_response)

	# test delete
	redis_driver.set(cache_key, cache_value)
	delete_response = redis_driver.delete(cache_key)
	ppp('delete_response:', delete_response)
	t.should_be_equal(expected=1, actual=delete_response)


# test batching
batch_set_response = redis_driver.batch_set(items=cache_items, ttl=cache_ttl)
ppp('batch_set_response:', batch_set_response)
batch_set_expected = {}
for key, val in cache_items.items():
	batch_set_expected[key] = True
t.should_be_equal(expected=batch_set_expected, actual=batch_set_response)

# test get of single after batch set
cache_key = 'string'
cache_value = cache_items[cache_key]
get_response = redis_driver.get(key=cache_key)
ppp('get_response:', get_response)
t.should_be_equal(expected=cache_value, actual=get_response)

cache_key_list = list(cache_items.keys())
batch_get_response = redis_driver.batch_get(keys=cache_key_list)
ppp('batch_get_response:', batch_get_response)
t.should_be_equal(expected=cache_items, actual=batch_get_response)

batch_delete_response = redis_driver.batch_delete(keys=cache_key_list)
ppp('batch_delete_response:', batch_delete_response)
batch_delete_expected = {}
for key, val in cache_items.items():
	batch_delete_expected[key] = 1
t.should_be_equal(expected=batch_delete_expected, actual=batch_delete_response)


######## TEST REDIS SPECIFIC METHODS ########


redis_driver.set(
	key='my_key',
	value='my_value',
	ttl=30
)
redis_keys = redis_driver.get_all_keys()
ppp('all currently set Redis keys:', redis_keys)


t.print_report()

