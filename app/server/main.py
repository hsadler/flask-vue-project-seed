
from random import randint
from flask import (
    Flask,
    render_template,
    jsonify
)

from api.web.wall_messages_api import web_wall_messages_api


# init Flask app instance
app = Flask(
    __name__,
    static_folder='../client/dist/static',
    template_folder='../client/dist'
)


# register api routes
app.register_blueprint(web_wall_messages_api, url_prefix='/api/wall-messages')


# sample API route
@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


# serve index for non-API calls
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)






