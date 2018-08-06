
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


# Steps:
# create a mysql test table test_user
# create test_user_data_object
# test base_data_object methods on test_user_data_object
# drop test table


######## CREATE TEST TABLE ########


TABLE_NAME = 'test_user'
create_table_query = """
	CREATE TABLE IF NOT EXISTS {0} (
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
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
	DEFAULT_CACHE_TTL = 30


######## TEST DATA OBJECT INTERFACE ########


user_data = {
	'name': 'Harry',
	'age': 36,
	'admin': True
}
test_user_DO = TestUserDataObject.create(prop_dict=user_data)
ppp(test_user_DO.to_dict())
t.should_be_equal(
	expected=user_data,
	actual=test_user_DO.to_dict()
)


# @classmethod
# def find_many(
# 	cls,
# 	prop_dict={},
# 	limit=None,
# 	db_driver_class=None,
# 	cache_driver_class=None
# ):


# @classmethod
# def find_one(
# 	cls,
# 	prop_dict={},
# 	db_driver_class=None,
# 	cache_driver_class=None,
# 	cache_ttl=None
# ):


# def get_prop(self, prop_name):


# def set_prop(self, prop_name, prop_value):


# def save(self, cache_ttl=None):


# def delete(self):


######## DELETE TEST TABLE ########


drop_table_query = """
	DROP TABLE {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)


t.print_report()

