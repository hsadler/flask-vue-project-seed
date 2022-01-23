
from flask import (
    Flask,
    render_template,
)

# init Flask app instance
app = Flask(
    __name__,
    static_folder='../client/dist/static',
    template_folder='../client/dist'
)


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


# serve index for non-API calls
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



