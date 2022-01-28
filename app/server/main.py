
from flask import Flask
from flask_cors import CORS

# init Flask app instance and configure CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# register api routes
from api.web.wall_messages_api import web_wall_messages_api
app.register_blueprint(web_wall_messages_api, url_prefix='/api/wall-messages')

# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



