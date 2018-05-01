
# Wall Messages Service

from data_object.wall_message_data_object import WallMessageDataObject


class WallMessages():
	"""
	Wall Messages Service

	"""

	@staticmethod
	def get_all():
		wms = WallMessageDataObject.find_many()
		return wms


	@staticmethod
	def add_message(message_body, message_attribution):
		wm = WallMessageDataObject.create(prop_dict={
			'message': message_body,
			'attribution': message_attribution
		})
		return wm.save();
