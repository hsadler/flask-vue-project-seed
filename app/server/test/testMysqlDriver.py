
import sys
# TODO: find a way to do this via a config which sets a project_dir
sys.path.append('..')

from datastore.driver.mysql_driver import MySqlDriver
from utils.print import ppp


mysql_driver = MySqlDriver(
	database_name='flask_vue_project_seed',
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
		'age': 66
	},
	where_props={
		'id': 1
	}
)
ppp(update_res)
sys.exit()

# test delete
mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props=[]
)


######## TEST DATABASE UTILS ########

size = mysql_driver.get_database_size()
ppp(size)

description = mysql_driver.describe_table(table_name="example")
ppp(description)




