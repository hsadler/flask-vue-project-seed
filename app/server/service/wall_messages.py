
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
	def find_one(message_id):
		wm = WallMessageDataObject.find_one(prop_dict={
			'id': message_id
		})
		return wm


	@staticmethod
	def add_message(message_body, message_attribution):
		wm = WallMessageDataObject.create(prop_dict={
			'message': message_body,
			'attribution': message_attribution
		})
		return wm.save();


	@staticmethod
	def update_message(message_id, message_body, message_attribution):
		wm = WallMessageDataObject.find_one(prop_dict={
			'id': message_id
		})
		wm.set_prop('message', message_body)
		wm.set_prop('attribution', message_attribution)
		return wm.save();
