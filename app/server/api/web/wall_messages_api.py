

# Wall Messages API

from flask import Blueprint, jsonify, request

from service.wall_messages import WallMessages
web_wall_messages_api = Blueprint('web_wall_messages_api', __name__)


@web_wall_messages_api.route('/get-all', methods=['GET'])
def get_all():
	"""
	Get all wall messages.

	"""

	wms = WallMessages.get_all()
	response = [ wm.to_dict() for wm in wms ]
	return jsonify(response)


@web_wall_messages_api.route('/find-one', methods=['GET'])
def find_one():
	"""
	Find a wall message by id.

	"""

	message_id = request.args.get('message_id')
	wm = WallMessages.find_one(message_id=message_id)
	return jsonify(wm.to_dict())


@web_wall_messages_api.route('/add-message', methods=['POST'])
def add_message():
	"""
	Add a wall message.

	"""

	r = request.get_json()
	message_body = r['message']
	message_attribution = r['attribution']
	wm = WallMessages.add_message(
		message_body=message_body,
		message_attribution=message_attribution
	)
	return jsonify(wm.to_dict())


@web_wall_messages_api.route('/update-message', methods=['POST'])
def update_message():
	"""
	Update a wall message.

	"""

	r = request.get_json()
	message_id = r['message_id']
	message_body = r['message_body']
	message_attribution = r['message_attribution']
	wm = WallMessages.update_message(
		message_id=message_id,
		message_body=message_body,
		message_attribution=message_attribution
	)
	return jsonify(wm.to_dict())



