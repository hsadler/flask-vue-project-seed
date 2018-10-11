
import sys
sys.path.append('..')

import uuid
import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.database_config.mysql.master_mysql_db import MasterMySqlDB
from testie import Testie
from utils.print import ppp


t = Testie()

mysql_driver = MySqlDriver(db_config=MasterMySqlDB.get_instance())


######## HELPER FUNCTIONS ########


def create_uuid():
	return uuid.uuid4().hex


######## TEST 'WHERE' CLAUSE BUILDER ########


where_clause, where_vals = MySqlDriver.construct_where_clause(where_props={
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

expected_where_clause = "WHERE `id` = %s AND `name` LIKE %s AND `age` > %s AND \
`age` <= %s AND `age` <> %s AND `height` IN (%s,%s,%s,%s) AND `race` IS NOT %s \
AND `maiden_name` IS %s"

t.should_be_equal(
	expected=expected_where_clause,
	actual=where_clause
)


######## TEST 'ORDER BY' CLAUSE BUILDER ########


order_by_field = 'uuid'
order_by_direction = 'descending'
order_by_clause = MySqlDriver.construct_order_by_clause(
	field=order_by_field,
	direction=order_by_direction
)
ppp('order by uuid descending clause:', order_by_clause)
t.should_be_equal(
	expected='ORDER BY {} {}'.format(order_by_field, 'DESC'),
	actual=order_by_clause
)

order_by_field = 'name'
order_by_direction = None
order_by_clause = MySqlDriver.construct_order_by_clause(
	field=order_by_field,
	direction=order_by_direction
)
ppp('order by name default order clause:', order_by_clause)
t.should_be_equal(
	expected='ORDER BY {}'.format(order_by_field),
	actual=order_by_clause
)

order_by_field = 'name'
order_by_direction = 'does not exist'
order_by_clause = MySqlDriver.construct_order_by_clause(
	field=order_by_field,
	direction=order_by_direction
)
ppp('order by name bad direction input clause:', order_by_clause)
t.should_be_equal(
	expected='ORDER BY {}'.format(order_by_field),
	actual=order_by_clause
)

order_by_field = 'name'
order_by_direction = 'whatever'
order_by_random = True
order_by_clause = MySqlDriver.construct_order_by_clause(
	field=order_by_field,
	direction=order_by_direction,
	random=True
)
ppp('order by random clause:', order_by_clause)
t.should_be_equal(
	expected='ORDER BY RAND()',
	actual=order_by_clause
)


######## CREATE TEST TABLE ########


TABLE_NAME = 'test_table'

# drop table just in case it exists
drop_table_query = """
	DROP TABLE IF EXISTS {0}
""".format(TABLE_NAME)
query_result = mysql_driver.query_bind(query_string=drop_table_query)
ppp('result of drop table query:', query_result)

# create test table
create_table_query = """
	CREATE TABLE IF NOT EXISTS {0} (
		uuid VARCHAR(32) PRIMARY KEY,
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
insert_uuid_1 = create_uuid()
insert_message_1 = 'hello!'
insert_attribution_1 = 'bot'
inserted_record_dict = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': insert_uuid_1,
		'message': insert_message_1,
		'attribution': insert_attribution_1
	}
)
ppp('inserted records dict:', inserted_record_dict)
t.should_be_equal(
	expected={
		'uuid': insert_uuid_1,
		'insert_message': insert_message_1,
		'insert_attribution': insert_attribution_1
	},
	actual={
		'uuid': inserted_record_dict['uuid'],
		'insert_message': inserted_record_dict['message'],
		'insert_attribution': inserted_record_dict['attribution']
	}
)


# test find
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'uuid': insert_uuid_1
	},
	limit=1
)
found_record = found_records[0]
ppp('found record:', found_record)
t.should_be_equal(
	expected=insert_message_1,
	actual=found_record['message']
)
t.should_be_equal(
	expected=insert_attribution_1,
	actual=found_record['attribution']
)

# do a bunch of inserts
insert_uuid_2 = create_uuid()
insert_message_2 = 'im a message'
insert_attribution_2 = 'jimmy'
inserted_record_dict = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': insert_uuid_2,
		'message': insert_message_2,
		'attribution': insert_attribution_2
	}
)
insert_uuid_3 = create_uuid()
insert_message_3 = 'anyone home?'
insert_attribution_3 = 'questioner man'
inserted_record_dict = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': insert_uuid_3,
		'message': insert_message_3,
		'attribution': insert_attribution_3
	}
)
insert_uuid_4 = create_uuid()
insert_message_4 = 'get off my lawn'
insert_attribution_4 = 'soldier76'
inserted_record_dict = mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': insert_uuid_4,
		'message': insert_message_4,
		'attribution': insert_attribution_4
	}
)

# test 'find_by_fields' with order_props
sorted_uuids = [insert_uuid_1, insert_uuid_2]
sorted_uuids.sort()
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'uuid': {
			'in': sorted_uuids
		}
	},
	order_props={
		'field': 'uuid'
	}
)
ppp('found records by 2 uuids:', found_records)
found_uuids = [ x['uuid'] for x in found_records ]
t.should_be_equal(
	expected=sorted_uuids,
	actual=found_uuids
)
# reversed order by uuid and 'order by' direction 'descending'
reverse_sorted_uuids = sorted_uuids.copy()
reverse_sorted_uuids.reverse()
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'uuid': {
			'in': sorted_uuids
		}
	},
	order_props={
		'field': 'uuid',
		'direction': 'desc'
	}
)
ppp('found records by 2 uuids:', found_records)
found_uuids = [ x['uuid'] for x in found_records ]
t.should_be_equal(
	expected=reverse_sorted_uuids,
	actual=found_uuids
)
# test 'find_by_fields' with random order
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={},
	order_props={
		'random': True
	},
	limit=3
)
ppp('found records by random:', found_records)
all_uuids = [ insert_uuid_1, insert_uuid_2, insert_uuid_3, insert_uuid_4 ]
found_uuids = [ x['uuid'] for x in found_records ]
t.should_be_equal(
	expected=[ True, True, True ],
	actual=[ (x in all_uuids) for x in found_uuids ]
)


# test update
new_insert_message = 'hello2!'
update_res = mysql_driver.update_by_fields(
	table_name=TABLE_NAME,
	value_props={
		'message': new_insert_message
	},
	where_props={
		'uuid': insert_uuid_1
	}
)
ppp(
	'rows affected: {0}'.format(update_res['rows_affected']),
	'updated_ts: {0}'.format(update_res['updated_ts'])
)
t.should_be_equal(
	expected=1,
	actual=update_res['rows_affected']
)
t.should_be_equal(
	expected=int,
	actual=type(update_res['updated_ts'])
)


# test delete
rows_deleted = mysql_driver.delete_by_fields(
	table_name=TABLE_NAME,
	where_props={
		'uuid': insert_uuid_1
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
		'uuid': create_uuid(),
		'message': None,
		'attribution': insert_attribution_1
	}
)
insert_attribution_2 = 'bot #2'
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': create_uuid(),
		'attribution': insert_attribution_2
	}
)
found_records = mysql_driver.find_by_fields(
	table_name=TABLE_NAME,
	where_props={ 'message': None }
)
ppp('found records:', found_records)
expected = [ insert_attribution_1, insert_attribution_2 ]
expected.sort()
actual = [
	x['attribution'] for x
	in found_records
	if x['attribution'] is not None
]
actual.sort()
t.should_be_equal(
	expected=expected,
	actual=actual
)
# test number where conditions
insert_amount_1 = 0
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': create_uuid(),
		'amount': insert_amount_1
	}
)
insert_amount_2 = 1
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': create_uuid(),
		'amount': insert_amount_2
	}
)
insert_amount_3 = -1
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': create_uuid(),
		'amount': insert_amount_3
	}
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
expected = [ insert_amount_1, insert_amount_2 ]
expected.sort()
actual = [ x['amount'] for x in found_records_2 ]
actual.sort()
t.should_be_equal(
	expected=expected,
	actual=actual
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
expected = [ insert_amount_1, insert_amount_3 ]
expected.sort()
actual = [ x['amount'] for x in found_records_3 ]
actual.sort()
t.should_be_equal(
	expected=expected,
	actual=actual
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
insert_uuid = create_uuid()
insert_message = 'i am the query bind!'
insert_attribution = 'mr. query bind'
mysql_driver.insert(
	table_name=TABLE_NAME,
	value_props={
		'uuid': insert_uuid,
		'message': insert_message,
		'attribution': insert_attribution
	}
)

# test query_bind method
bind_vars = {
	'uuid': insert_uuid,
	'limit': 5
}
select_query = 'SELECT * FROM {0} WHERE uuid = :uuid LIMIT :limit'.format(
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

