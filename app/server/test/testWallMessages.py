
import sys
sys.path.append('..')

from service.wall_messages import WallMessages
from testie import Testie
from utils.print import ppp


"""
Test WallMessages service.

Requires creation of 'wall_message' MySQL table via
create-wall-messages-table.py script.
"""


t = Testie()


message_body = 'hello, world!'
message_attribution = 'harry'
added_wm = WallMessages.add_message(
	message_body=message_body,
	message_attribution=message_attribution
)

ppp(['added wall message:', added_wm.to_dict()])

t.should_be_equal(
	expected=message_body,
	actual=added_wm.get_prop('message')
)
t.should_be_equal(
	expected=message_attribution,
	actual=added_wm.get_prop('attribution')
)


found_wm = WallMessages.find_one(message_id=added_wm.get_prop('id'))

ppp(['found wall message:', found_wm.to_dict()])

t.should_be_equal(
	expected=added_wm.to_dict(),
	actual=found_wm.to_dict()
)


updated_message_body = 'i am the new message'
updated_message_attribution = 'newman'
updated_wm = WallMessages.update_message(
	message_id=added_wm.get_prop('id'),
	message_body=updated_message_body,
	message_attribution=updated_message_attribution
)

ppp(['updated wall message:', updated_wm.to_dict()])

t.should_be_equal(
	expected=updated_message_body,
	actual=updated_wm.get_prop('message')
)
t.should_be_equal(
	expected=updated_message_attribution,
	actual=updated_wm.get_prop('attribution')
)


delete_status = WallMessages.delete_message(
	message_id=added_wm.get_prop('id')
)

ppp('deleted wall message successfully: {0}'.format(delete_status))

t.should_be_equal(expected=True, actual=delete_status)


wms = WallMessages.get_all()
ppp(['all wall messages:', [ wm.to_dict() for wm in wms ]])


t.print_report()

