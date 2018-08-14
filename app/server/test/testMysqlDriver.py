
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
		attribution VARCHAR(255),
		amount INT(11)
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


# test IS NULL where condition
insert_attribution_1 = 'bot #1'
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'message': None,
		'attribution': insert_attribution_1
	}
)
insert_attribution_2 = 'bot #2'
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={ 'attribution': insert_attribution_2 }
)
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={ 'message': None }
)
ppp('found records:', found_records)
t.should_be_equal(
	expected=[ insert_attribution_1, insert_attribution_2 ],
	actual=[ x['attribution'] for x in found_records ]
)
# test number where conditions
insert_amount_1 = 0
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={ 'amount': insert_amount_1 }
)
insert_amount_2 = 1
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={ 'amount': insert_amount_2 }
)
insert_amount_3 = -1
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={ 'amount': insert_amount_3 }
)
found_records_1 = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'amount': {
			'>': 0
		}
	}
)
ppp('found records 1:', found_records_1)
t.should_be_equal(
	expected=[ insert_amount_2 ],
	actual=[ x['amount'] for x in found_records_1 ]
)
found_records_2 = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'amount': {
			'>=': 0
		}
	}
)
ppp('found records 2:', found_records_2)
t.should_be_equal(
	expected=[ insert_amount_1, insert_amount_2 ],
	actual=[ x['amount'] for x in found_records_2 ]
)
found_records_3 = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'amount': {
			'lte': 0
		}
	}
)
ppp('found records 3:', found_records_3)
t.should_be_equal(
	expected=[ insert_amount_1, insert_amount_3 ],
	actual=[ x['amount'] for x in found_records_3 ]
)
# test NOT IN conditional
found_records_4 = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'amount': {
			'not in': [1, -1]
		}
	}
)
ppp('found records 4:', found_records_4)
t.should_be_equal(
	expected=[ insert_amount_1 ],
	actual=[ x['amount'] for x in found_records_4 ]
)


######## TEST MYSQL SPECIFIC METHODS ########


# insert
insert_message = 'i am the query bind!'
insert_attribution = 'mr. query bind'
mysql_driver.insert(
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

ppp('result of select query:', select_query_result)


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





