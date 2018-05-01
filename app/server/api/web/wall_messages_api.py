
from flask import Blueprint, jsonify

from service.wall_messages import WallMessages


web_wall_messages_api = Blueprint('web_wall_messages_api', __name__)


@web_wall_messages_api.route('/get-all')
def get_all():
	wms = WallMessages.get_all()
	response = [ wm.to_dict() for wm in wms ]
	return jsonify(response)
