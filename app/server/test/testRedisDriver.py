
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


cache_key = 'my key'
cache_values = [
	'my_value',
	1234,
	-1.234,
	True,
	[1, 'cats', False],
	{'one': 1}
]
cache_ttl = 1


for cache_value in cache_values:


	# test set
	set_response = redis_driver.set(
		key=cache_key,
		value=cache_value,
		ttl=cache_ttl
	)

	ppp(['set_response:', set_response])

	t.should_be_equal(expected=True, actual=set_response)


	# test get before expiration
	get_response = redis_driver.get(key=cache_key)

	ppp(['get_response:', get_response])

	t.should_be_equal(expected=cache_value, actual=get_response)


	# test get after expiration
	time.sleep(2)
	get_response = redis_driver.get(key=cache_key)

	ppp(['get_response:', get_response])

	t.should_be_equal(expected=None, actual=get_response)


	# test delete
	redis_driver.set(cache_key, cache_value)
	delete_response = redis_driver.delete(cache_key)

	ppp(['delete_response:', delete_response])

	t.should_be_equal(expected=1, actual=delete_response)


######## TEST REDIS SPECIFIC METHODS ########


redis_driver.set(
	key='my_key',
	value='my_value',
	ttl=30
)

redis_keys = redis_driver.get_all_keys()

ppp(['all currently set Redis keys:', redis_keys])


t.print_report()

