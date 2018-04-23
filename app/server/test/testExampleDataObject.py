
import sys
sys.path.append('..')

from data_object.example_data_object import ExampleDataObject
from utils.print import ppp


######## TEST DATA OBJECT INTERFACE ########

# test create
created_example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'hello world!' }
)
ppp(['created example data object: ', created_example_DO.get_state()])

# test find_many
found_example_DOs = ExampleDataObject.find_many(
	prop_dict={ 'field': 'hello world!' },
	limit=3
)
ppp('found example data objects:')
for ex_DO in found_example_DOs:
	ppp(ex_DO.get_state())

# test find_one
found_example_DO = ExampleDataObject.find_one(
	prop_dict={'id': 1}
)
ppp(['found one example data object: ', found_example_DO.get_state()])

# test get_prop
property_name = 'field'
property_value = found_example_DO.get_prop(prop_name=property_name)
ppp('retrieved property "key"->{0}, "value"->{1}'.format(
	property_name,
	property_value
))

# test set_prop
property_name = 'field'
property_value = 'hi there again!'
found_example_DO.set_prop(
	prop_name=property_name,
	prop_value=property_value
)
ppp([
	'set property "key"->{0}, "value"->{1} for example data object:'.format(
		property_name,
		property_value
	),
	found_example_DO.get_state()
])

# test save
saved_example_DO = found_example_DO.save()
ppp(['saved example data object:', saved_example_DO.get_state()])

# test delete
to_delete_example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'delete me...' }
)
to_delete_example_DO = to_delete_example_DO.save()
ppp(['data object to delete:', to_delete_example_DO.get_state()])
record_was_deleted = to_delete_example_DO.delete()
ppp('record was deleted: {0}'.format(record_was_deleted))

