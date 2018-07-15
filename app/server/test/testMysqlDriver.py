
import sys
sys.path.append('..')

import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from testie import Testie
from utils.print import ppp


################################################################################
### REWRITE TO DO THIS:
###		- create a DB table
###		- create a populate with records
###		- run tests
###		- delete table
################################################################################


t = Testie()

mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)


######## TEST CRUD INTERFACE ########


TABLE_NAME = 'wall_message'

# test insert
insert_message = 'hello!'
insert_attribution = 'bot'
insert_id = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'message': insert_message,
		'attribution': insert_attribution
	}
)

ppp('insert id: {0}'.format(insert_id))

t.should_be_equal(
	expected=int,
	actual=type(insert_id)
)


# test read
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'id': insert_id
	},
	limit=1
)
found_record = found_records[0]

ppp(['found record:', found_record])

t.should_be_equal(
	expected=insert_message,
	actual=found_record['message']
)
t.should_be_equal(
	expected=insert_attribution,
	actual=found_record['attribution']
)


# test update
new_insert_message = 'hello2!'
rows_updated = mysql_driver.update_by_fields(
	table_name=TABLE_NAME,
	value_props={
		'message': new_insert_message
	},
	where_props={
		'id': insert_id
	}
)

ppp('rows updated: {0}'.format(rows_updated))

t.should_be_equal(
	expected=1,
	actual=rows_updated
)


# test delete
rows_deleted = mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'id': insert_id
	}
)

ppp('rows deleted: {0}'.format(rows_deleted))

t.should_be_equal(
	expected=1,
	actual=rows_deleted
)


######## TEST MYSQL SPECIFIC METHODS ########


query_id = 0
query_limit = 5
select_query = 'SELECT * FROM {0} WHERE id > {1} LIMIT {2}'.format(
	TABLE_NAME,
	query_id,
	query_limit
)
select_query_result = mysql_driver.query(query_string=select_query)

ppp(['result of select query:', select_query_result])


######## TEST TABLE UTILS ########


description = mysql_driver.describe_table(table_name=TABLE_NAME)
ppp(['table description:', description])


table_field_names = mysql_driver.get_table_field_names(table_name=TABLE_NAME)
ppp(['table field names:', table_field_names])


######## TEST DATABASE UTILS ########


db_size = mysql_driver.get_database_size()
ppp(['database size: ', db_size])


t.print_report()





