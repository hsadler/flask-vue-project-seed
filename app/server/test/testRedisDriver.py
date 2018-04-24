
import sys
sys.path.append('..')

import config.config as config
from data_store.cache_driver.redis_driver import RedisDriver
from utils.print import ppp


redis_driver = RedisDriver()


######## TEST INTERFACE ########

key = 'my key'
value = 'my value'

# test set
set_response = redis_driver.set(key, value)
ppp(['set_response:', set_response])

# test get
get_response = redis_driver.get(key)
ppp(['get_response:', get_response])

# test delete
delete_response = redis_driver.delete(key)
ppp(['delete_response:', delete_response])