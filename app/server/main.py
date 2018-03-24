
from random import randint
from flask import (
    Flask,
    render_template,
    jsonify
)


# init Flask app instance
app = Flask(
    __name__,
    static_folder='../client/dist/static',
    template_folder='../client/dist'
)


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






