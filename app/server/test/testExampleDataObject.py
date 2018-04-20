
import sys
sys.path.append('..')

from data_object.example_data_object import ExampleDataObject
from utils.print import ppp


######## TEST DATA OBJECT INTERFACE ########

# test create
created_example_DO = ExampleDataObject.create(
	prop_dict={ 'field': 'hello world!' }
)
ppp(created_example_DO)

# test find_many
found_example_DOs = ExampleDataObject.find_many(
	prop_dict={ 'field': 'hello world!' },
	limit=3
)
ppp(found_example_DOs)

# test find_one
found_example_DO = ExampleDataObject.find_one(
	prop_dict={'id': 1}
)
ppp(found_example_DO)

# test get_prop
field_value = found_example_DO.get_prop(prop_name='field')
ppp(field_value)

# test set_prop
found_example_DO.set_prop(
	prop_name='field',
	prop_value='hi there again!'
)
ppp(found_example_DO)

# test save
res = found_example_DO.save()
ppp(res)

# test delete
res = found_example_DO.delete()
ppp(res)

