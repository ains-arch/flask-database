import os
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


def are_credentials_good(username, password):
    if username == 'haxor' and password == '1337':
        return True
    else:
        return False
    # FIXME:
    # look into db and check if the password is correct for the user


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def root():
    print_debug_info()

    messages = [{}]

    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)

    return render_template('root.html', logged_in=good_credentials, messages=messages)

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

def print_debug_info():
    # GET method
    print('request.args.get("username")=', request.args.get("username"))
    print('request.args.get{"password"}=', request.args.get("password"))

    # POST method
    print('request.form.get{"username"}=', request.form.get("username"))
    print('request.form.get{"password"}=', request.form.get("password"))

    # cookies
    print('request.cookies.get{"username"}=', request.cookies.get("username"))
    print('request.cookies.get{"password"}=', request.cookies.get("password"))

@app.route("/login", methods=["GET", "POST"])
def login():
    print_debug_info()

    username = request.form.get("username")
    password = request.form.get("password")

    print('username=', username)
    print('password=', password)

    good_credentials = are_credentials_good(username, password)
    print('good credentials=', good_credentials)

    if username is None:
        return render_template('login.html', bad_credentials=False)
    else:
        if not good_credentials:
            return render_template('login.html', bad_credentials=True)
        else:
            template = render_template(
                    'login.html',
                    bad_credentials=False,
                    logged_in=True)
            response = make_response(template)
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response

    return render_template('login.html')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    pass


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    pass


@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    pass


@app.route("/search", methods=["GET", "POST"])
def search():
    pass
