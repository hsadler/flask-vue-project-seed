
import sys
sys.path.append('..')

import config.config as config
from data_store.database_driver.mysql_driver import MySqlDriver
from data_store.database_config.mysql.master_mysql_db import MasterMySqlDB
from utils.print import ppp


mysql_driver = MySqlDriver(db_config=MasterMySqlDB.get_instance())

create_table_query = """
	CREATE TABLE IF NOT EXISTS wall_message (
		uuid VARCHAR(32) PRIMARY KEY,
		created_ts INT(11) NOT NULL,
		updated_ts INT(11) NOT NULL,
		message VARCHAR(1000),
		attribution VARCHAR(255)
	)
"""

query_result = mysql_driver.query_bind(query_string=create_table_query)

ppp('result of create table query:', query_result)
