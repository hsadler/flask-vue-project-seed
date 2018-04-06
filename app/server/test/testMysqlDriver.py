
import sys
# TODO: find a way to do this via a config which sets a project_dir
sys.path.append('..')

from datastore.driver.mysql_driver import MySQLdbDriver


mysql_driver = MySQLdbDriver(
	database_name='flask_vue_project_seed',
)

size = mysql_driver.get_size('example')

print(size)

# create table example(
# 	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# 	example_column VARCHAR(255)
# );

