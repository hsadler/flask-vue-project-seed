
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


######## CREATE TEST TABLE ########


TABLE_NAME = 'test_user'
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


######## TEST DATA OBJECT INTERFACE ########


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


# test 'find_many' method
find_id = test_user_DO.get_prop('uuid')
found_test_user_DOs = TestUserDataObject.find_many(prop_dict={ 'uuid': find_id })
found_test_user_DO = found_test_user_DOs[0]
ppp("'find_many' method data object:", found_test_user_DO.to_dict())
t.should_be_equal(
	expected=test_user_DO.to_dict(),
	actual=found_test_user_DO.to_dict()
)

sys.exit()


# test 'find_one' method
found_test_user_DO = TestUserDataObject.find_one(prop_dict={ 'id': find_id })
ppp("'find_one' method data object:", found_test_user_DO.to_dict())
t.should_be_equal(
	expected=test_user_DO.to_dict(),
	actual=found_test_user_DO.to_dict()
)


# test 'get_prop' method
DO_name = found_test_user_DO.get_prop(prop_name='name')
ppp("'get_prop' method name:", DO_name)
t.should_be_equal(
	expected=user_data['name'],
	actual=DO_name
)


# test 'set_prop' method
new_age = 101
set_prop_res = found_test_user_DO.set_prop(prop_name='age', prop_value=new_age)
ppp("'set_prop' res:", set_prop_res)
ppp("test user data object after 'set_prop':", found_test_user_DO.to_dict())
t.should_be_equal(
	expected=new_age,
	actual=found_test_user_DO.get_prop(prop_name='age')
)


# test 'delete' method
delete_res = found_test_user_DO.delete()
ppp("'delete' res:", delete_res)
t.should_be_equal(
	expected=bool,
	actual=type(delete_res)
)


######## DELETE TEST TABLE ########


drop_table_query = """
	DROP TABLE {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)


t.print_report()

