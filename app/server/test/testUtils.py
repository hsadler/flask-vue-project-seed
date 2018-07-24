
import sys
sys.path.append('..')

from utils.print import ppp


my_int = 123
ppp(my_int, my_int)


my_list = ['hi', 'there']
ppp(my_list, my_list)
ppp(my_list, my_list, as_json=1)


my_tuple = (1.23, 'hello', False)
ppp(my_tuple, my_tuple)
ppp(my_tuple, my_tuple, as_json=1)


my_dict = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9
}
ppp(my_dict, my_dict)
ppp(my_dict, my_dict, as_json=1)


class MyClass():
	def __init__(self, prop_1):
		self.prop_1 = prop_1

my_instance = MyClass(prop_1='im a prop')

ppp(my_instance, my_instance)
try:
	ppp(my_instance, my_instance, as_json=1)
except:
	ppp('WARNING: cannot json serialize a python object...')


