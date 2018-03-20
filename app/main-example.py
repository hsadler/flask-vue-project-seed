
import random

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


# init Flask instance
app = Flask(__name__)


################## ROUTE EXAMPLES ##################

# index
@app.route('/')
def index():
    return 'I\'m the index.'

# named route
@app.route('/hello')
def hello_world():
    return 'Hello, World!'

# dynamic route
@app.route('/profile/<username>')
def profile(username):
    return 'Profile for "%s"' % username

# typed/converted variables
@app.route('/userpage/<username>/<int:page_number>')
def userpage(username, page_number):
    return  username + "'s page number: " + str(page_number)

# specify GET, POST, etc.
@app.route('/get-or-post', methods=['GET', 'POST'])
def get_or_post():
    if request.method == 'GET':
        return 'A GET request was made..'
    elif request.method == 'POST':
        return 'A POST request was made..'

# access GET params
# http://localhost:5000/get-params?x=1&y=2
@app.route('/get-params', methods=['GET'])
def get_params():
    param_x = int(request.args.get('x'))
    param_y = int(request.args.get('y'))
    summed = str(param_x + param_y)
    return 'Addition of GET params: %s + %s = %s' % (param_x, param_y, summed)

# access POST params
# curl -X POST -F 'x=2' -F 'y=3' http://localhost:5000/post-params
@app.route('/post-params', methods=['POST'])
def post_params():
    param_x = int(request.form['x'])
    param_y = int(request.form['y'])
    summed = str(param_x + param_y)
    return 'Addition of POST params: %s + %s = %s' % (param_x, param_y, summed)

# dynamically rendered template
@app.route('/dynamic-hello/')
@app.route('/dynamic-hello/<name>')
def dynamic_hello(name=None):
    return render_template('dynamic-hello.html', name=name)

# template with dynamic markup
@app.route('/dynamic-markup')
def dynamic_markup():
    rand = random.randint(1, 100)
    markup = Markup('<span style="color: green">%s</span>') % str(rand)
    return render_template('dynamic-markup.html', markup=markup)

# route to be redirected from
@app.route('/redirect-from')
def redirect_from():
    return redirect(url_for('redirect_to'))

# route to be redirected to
@app.route('/redirect-to')
def redirect_to():
    return 'You have been redirected..'

# abort and send status code
@app.route('/res-code')
def res_code():
    abort(401)
    return 'Never got here..'

# custom error page (also shows how to send a static file)
@app.errorhandler(401)
def unauthorized(error):
    return app.send_static_file('unauthorized.html'), 401

# sessions
@app.route('/check-session')
def check_session():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

# login with username and set on session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('check_session'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

# logout and remove username from session
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('check_session'))

# set the secret key for sessions
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# note: generate a good key with:
# import os
# os.urandom(24)

# logging example
@app.route('/logging')
def logging():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return 'There are now logs in the CLI'

####################################################


# run the app if executed as main file to python interpreter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
