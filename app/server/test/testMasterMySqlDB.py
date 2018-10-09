
import sys
sys.path.append('..')

from data_store.database_config.mysql.master_mysql_db import MasterMySqlDB
from testie import Testie
from utils.print import ppp


t = Testie()


master_db_instance_1 = MasterMySqlDB.get_instance()
master_db_instance_2 = MasterMySqlDB.get_instance()

ppp('master_db_instance_1:', master_db_instance_1)
ppp('master_db_instance_2:', master_db_instance_2)

t.should_be_equal(
	actual=True,
	expected=master_db_instance_1 == master_db_instance_2
)


db = MasterMySqlDB.get_instance()
TABLE_NAME = 'test_table'


# test table deletion
drop_table_query = """
	DROP TABLE IF EXISTS {0}
""".format(TABLE_NAME)

db.cur.execute(drop_table_query)
res = db.cur.fetchall()
ppp('drop table query response:', res)
t.should_be_equal(actual=type(res), expected=tuple)
t.should_be_equal(actual=len(res), expected=0)


# test table creation
create_table_query = """
	CREATE TABLE IF NOT EXISTS {0} (
		message VARCHAR(255),
		attribution VARCHAR(255),
		amount INT(11)
	)
""".format(TABLE_NAME)
db.cur.execute(create_table_query)
res = db.cur.fetchall()
rows_affected = db.cur.rowcount
ppp('create table query response:', res)
ppp('create table rows affected:', rows_affected)
t.should_be_equal(actual=type(res), expected=tuple)
t.should_be_equal(actual=len(res), expected=0)
t.should_be_equal(actual=rows_affected, expected=0)


# test record insert
record = {
	'message': 'hi there',
	'attribution': 'bot',
	'amount': 101
}
record_keys = list(record.keys())
record_values = list(record.values())
insert_query = """
	INSERT INTO {0} ({1}, {2}, {3})
	VALUES ('{4}', '{5}', {6});
""".format(
	TABLE_NAME,
	record_keys[0],
	record_keys[1],
	record_keys[2],
	record_values[0],
	record_values[1],
	record_values[2]
)
db.cur.execute(insert_query)
res = db.cur.fetchall()
rows_affected = db.cur.rowcount
ppp('insert query response:', res)
ppp('insert rows affected:', rows_affected)
t.should_be_equal(actual=type(res), expected=tuple)
t.should_be_equal(actual=len(res), expected=0)
t.should_be_equal(actual=rows_affected, expected=1)


# test record select
select_query = """
	SELECT * FROM {0};
""".format(TABLE_NAME)
db.cur.execute(select_query)
res = db.cur.fetchall()
rows_affected = db.cur.rowcount
ppp('select query response:', res)
ppp('select rows affected:', rows_affected)
t.should_be_equal(actual=type(res), expected=tuple)
t.should_be_equal(actual=len(res), expected=1)
found_record = res[0]
t.should_be_equal(actual=type(found_record), expected=dict)
t.should_be_equal(actual=found_record == record, expected=True)


t.print_report()

