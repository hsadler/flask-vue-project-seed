
from flask import (
    Flask,
    request,
    render_template,
    Markup,
    redirect,
    abort,
    url_for,
    session,
    escape
)


# init Flask app instance
app = Flask(
    __name__,
    static_folder='./dist/static',
    template_folder='./dist'
)


# routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
