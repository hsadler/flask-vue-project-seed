
import sys
sys.path.append('..')

import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from utils.print import ppp


mysql_driver = MySqlDriver(
	database_name=config.MYSQL_DB_NAME
)

create_table_query = """
	CREATE TABLE IF NOT EXISTS wall_message (
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
		created_ts INT(11) NOT NULL,
		updated_ts INT(11) NOT NULL,
		message VARCHAR(1000),
		attribution VARCHAR(255)
	)
"""
query_result = mysql_driver.query(query_string=create_table_query)

ppp(['result of create table query:', query_result])
