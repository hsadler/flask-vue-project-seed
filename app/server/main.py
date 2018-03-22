
import requests

from flask import (
    Flask,
    render_template
)


# init Flask app instance
app = Flask(
    __name__,
    static_folder='../client/dist/static',
    template_folder='../client/dist'
)


# serve dev or prod index
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    else:
        return render_template('index.html')


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
