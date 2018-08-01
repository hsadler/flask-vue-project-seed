
import sys
sys.path.append('..')

from testie import Testie
from utils.print import ppp


"""
Test Base Data Object.

"""


t = Testie()

mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)


# Steps:
# create a mysql test_table
# create test_data_object
# test base_data_object methods on test_data_object
# drop mysql table


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




t.print_report()

