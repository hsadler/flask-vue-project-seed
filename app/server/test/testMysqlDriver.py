
import sys
sys.path.append('..')

import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from testie import Testie
from utils.print import ppp


t = Testie()

mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)


######## TEST WHERE CLAUSE BUILDER ########


where_clause, where_vals = mysql_driver.construct_where_clause(where_props={
	'id': 1,
	'name': {
		'like': '%Sh%'
	},
	'age': {
		'gt': 20,
		'lte': 40,
		'!=': 30
	},
	'height': {
		'in': [1,2,3,4]
	},
	'race': {
		'is not': None
	},
	'maiden_name': None
})

ppp('where_clause:', where_clause)
ppp('where_vals:', where_vals)

expected_where_clause = "WHERE `id` = %s AND `name` LIKE %s AND `age` > %s AND \
`age` <= %s AND `age` <> %s AND `height` IN (%s,%s,%s,%s) AND `race` IS NOT %s \
AND `maiden_name` IS %s"

t.should_be_equal(
	expected=expected_where_clause,
	actual=where_clause
)


######## CREATE TEST TABLE ########


TABLE_NAME = 'test_table'
create_table_query = """
	CREATE TABLE IF NOT EXISTS {0} (
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
		created_ts INT(11) NOT NULL,
		updated_ts INT(11) NOT NULL,
		message VARCHAR(1000),
		attribution VARCHAR(255)
	)
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=create_table_query)
ppp('result of create table query:', query_result)


######## TEST CRUD INTERFACE ########


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


# test find
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'id': {
			'>': 0
		}
	},
	limit=1
)
found_record = found_records[0]

ppp('found record:', found_record)

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


# insert
insert_message = 'i am the query bind!'
insert_attribution = 'mr. query bind'
insert_id = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'message': insert_message,
		'attribution': insert_attribution
	}
)

# test query_bind method
bind_vars = {
	'id': 0,
	'limit': 5
}
select_query = 'SELECT * FROM {0} WHERE id > :id LIMIT :limit'.format(
	TABLE_NAME
)
select_query_result = mysql_driver.query_bind(
	query_string=select_query,
	bind_vars=bind_vars
)

ppp(['result of select query:', select_query_result])


######## TEST TABLE UTILS ########


description = mysql_driver.describe_table(table_name=TABLE_NAME)
ppp(['table description:', description])


table_field_names = mysql_driver.get_table_field_names(table_name=TABLE_NAME)
ppp(['table field names:', table_field_names])


######## TEST DATABASE UTILS ########


db_size = mysql_driver.get_database_size()
ppp(['database size: ', db_size])


######## DELETE TEST TABLE ########


drop_table_query = """
	DROP TABLE {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)


t.print_report()





