
import sys
# TODO: find a way to do this via a config which sets a project_dir
sys.path.append('..')

from datastore.driver.mysql_driver import MySqlDriver
from utils.print import ppp


mysql_driver = MySqlDriver(
	database_name='flask_vue_project_seed',
)


######## TEST DATABASE UTILS ########

size = mysql_driver.get_database_size()
ppp(size)

description = mysql_driver.describe_table(table_name="example")
ppp(description)


######## TEST CRUD INTERFACE ########

TABLE_NAME = 'person'

# test insert
insert_res = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'name': 'Wanda Bob',
		'age': 44,
		'male': False
	}
)
ppp(insert_res)

# test read
find_res = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'name': 'Wanda Bob'
	}
)
ppp(find_res)
sys.exit()

# test update
mysql_driver.update_by_fields(
	table_name=TABLE_NAME,
	value_props=[],
	where_props=[]
)

# test delete
mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props=[]
)






