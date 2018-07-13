
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
	set_response = redis_driver.set_single(
		key=cache_key,
		value=cache_value,
		ttl=cache_ttl
	)
	ppp(['set_response:', set_response])
	t.should_be_equal(expected=True, actual=set_response)

	# test get before expiration
	get_response = redis_driver.get_single(key=cache_key)
	ppp(['get_response:', get_response])
	t.should_be_equal(expected=cache_value, actual=get_response)

	# test get after expiration
	time.sleep(2)
	get_response = redis_driver.get_single(key=cache_key)
	ppp(['get_response:', get_response])
	t.should_be_equal(expected=None, actual=get_response)

	# test delete
	redis_driver.set_single(cache_key, cache_value)
	delete_response = redis_driver.delete_single(cache_key)
	ppp(['delete_response:', delete_response])
	t.should_be_equal(expected=1, actual=delete_response)

# test batching
batch_set_response = redis_driver.set_batch(items=cache_items, ttl=cache_ttl)
t.should_be_equal(expected=True, actual=batch_set_response)
# ....stopped here......

######## TEST REDIS SPECIFIC METHODS ########


redis_driver.set_single(
	key='my_key',
	value='my_value',
	ttl=30
)
redis_keys = redis_driver.get_all_keys()
ppp(['all currently set Redis keys:', redis_keys])


t.print_report()

