
import sys
# TODO: find a way to do this via a config which sets a project_dir
sys.path.append('..')

from datastore.driver.mysql_driver import MySqlDriver


mysql_driver = MySqlDriver(
	database_name='flask_vue_project_seed',
)


######## TEST TABLE UTILS ########

size = mysql_driver.get_database_size()
print(size)

description = mysql_driver.describe_table(table_name="example")
print(description)


######## TEST CRUD INTERFACE ########

TABLE_NAME = 'example'

# test create
mysql_driver.insert(
    table_name=TABLE_NAME,
    value_props=[]
)

# test read
mysql_driver.find_by_fields(
    table_name=TABLE_NAME,
    where_props=[]
)

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






