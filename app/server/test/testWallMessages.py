
import sys
sys.path.append('..')

from service.wall_messages import WallMessages
from utils.print import ppp


"""
Test WallMessages service.

Requires creation of 'wall_message' MySQL table via
create-wall-messages-table.py script.
"""


wm = WallMessages.add_message(
	message_body='hello, world!',
	message_attribution='harry'
)
ppp(['added wall message:', wm.to_dict()])


wms = WallMessages.get_all()
ppp(['all wall messages:', [ wm.to_dict() for wm in wms ]])