
import sys
sys.path.append('..')

import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from utils.print import ppp


mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)


######## TEST CRUD INTERFACE ########

TABLE_NAME = 'person'

# test insert
insert_id = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'name': 'Tim Tim',
		'age': 30,
		'male': True
	}
)
ppp('insert id: ' + str(insert_id))

# test read
found_record = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'name': 'Wanda Bob',
		'male': False
	},
	limit=2
)
ppp(['found record:', found_record])

# test update
rows_updated = mysql_driver.update_by_fields(
	table_name=TABLE_NAME,
	value_props={
		'name': 'Tim Timmy'
	},
	where_props={
		'age': 30
	}
)
ppp('rows updated: ' + str(rows_updated))

# test delete
rows_deleted = mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'id': 2
	}
)
ppp('rows deleted: ' + str(rows_deleted))


######## TEST TABLE UTILS ########

description = mysql_driver.describe_table(table_name="example")
ppp(['table description:', description])

table_field_names = mysql_driver.get_table_field_names(table_name='example')
ppp(['table field names:', table_field_names])


######## TEST DATABASE UTILS ########

db_size = mysql_driver.get_database_size()
ppp(['database size: ', db_size])





