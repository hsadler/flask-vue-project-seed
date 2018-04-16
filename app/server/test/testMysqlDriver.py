
import sys
sys.path.append('..')

import config.config as config
from datastore.database_driver.mysql_driver import MySqlDriver
from utils.print import ppp


mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME,
)


######## TEST CRUD INTERFACE ########

TABLE_NAME = 'person'

# test insert
insert_res = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'name': 'Tim Tim',
		'age': 30,
		'male': True
	}
)
ppp(insert_res)

# test read
find_res = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'name': 'Wanda Bob',
		'male': False
	},
	limit=2
)
ppp(find_res)

# test update
update_res = mysql_driver.update_by_fields(
	table_name=TABLE_NAME,
	value_props={
		'age': 20
	},
	where_props={
		'age': 1000
	}
)
ppp(update_res)

# test delete
delete_res = mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'id': 2
	}
)
ppp(delete_res)


######## TEST DATABASE UTILS ########

size = mysql_driver.get_database_size()
ppp(size)

description = mysql_driver.describe_table(table_name="example")
ppp(description)




