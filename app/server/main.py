
from flask import (
    Flask,
    jsonify
)

# init Flask app instance
app = Flask(__name__)


# ping route for testing
@app.route('/api/ping', methods=['GET'])
def handle_ping():
    from api.web.wall_messages_api import get_all
    from utils.print import ppp
    all = get_all()
    # TODO: check to see if this works later
    ppp(all)
    return all


# register api routes
from api.web.wall_messages_api import web_wall_messages_api
app.register_blueprint(web_wall_messages_api, url_prefix='/api/wall-messages')


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



