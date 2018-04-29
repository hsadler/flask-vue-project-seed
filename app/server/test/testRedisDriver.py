
import time
import sys
sys.path.append('..')

import config.config as config
from data_store.cache_driver.redis_driver import RedisDriver
from utils.print import ppp


redis_driver = RedisDriver()


######## TESTING SETUP ########

tests_passed = 0
tests_failed = 0

def test_should_equal(test_val, expected_val):
	global tests_passed
	global tests_failed
	if test_val == expected_val:
		tests_passed = tests_passed + 1
	else:
		tests_failed = tests_failed + 1
		ppp('test_val: {0} should have equaled expected_val: {1}'.format(
			test_val,
			expected_val
		))


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
	test_should_equal(set_response, True)
	ppp(['set_response:', set_response])

	# test get before expiration
	get_response = redis_driver.get(key=cache_key)
	test_should_equal(get_response, cache_value)
	ppp(['get_response:', get_response])

	# test get after expiration
	time.sleep(2)
	get_response = redis_driver.get(key=cache_key)
	test_should_equal(get_response, None)
	ppp(['get_response:', get_response])

	# test delete
	redis_driver.set(cache_key, cache_value)
	delete_response = redis_driver.delete(cache_key)
	test_should_equal(delete_response, 1)
	ppp(['delete_response:', delete_response])


######## DISPLAY TEST RESULTS ########

# test results
ppp('tests passed: {}'.format(tests_passed))
ppp('tests failed: {}'.format(tests_failed))


######## TEST REDIS SPECIFIC METHODS ########

redis_driver.set(
	key='my_key',
	value='my_value',
	ttl=30
)
redis_keys = redis_driver.get_all_keys()
ppp(['all currently set Redis keys:', redis_keys])


