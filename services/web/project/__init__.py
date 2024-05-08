import os
from sqlalchemy import text
from datetime import datetime

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    make_response
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import sqlalchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
psql_connection = "postgresql://hello_flask:hello_flask@dbd:5432"

class User(db.Model):
    __tablename__ = "users"

    id_users = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    id_urls = db.Column(db.Integer)

    def __init__(self, name, password):
        self.name = name
        self.password = password

def are_credentials_good(username, password):
    engine = sqlalchemy.create_engine(psql_connection)
    with engine.connect() as connection:
        # Prepare and execute the SQL command
        sqlcommand = "SELECT password FROM users WHERE name = :name"
        result = connection.execute(text(sqlcommand), {'name': username}).fetchone()

        # Check if the user was found and the password matches
        if result and result[0] == password:
            return True

@app.route("/")
def root():
    page = request.args.get('page', 1, type=int)
    messages_per_page = 20
    offset = (page - 1) * messages_per_page

    sqlcommand = """
    SELECT t.text, t.created_at, u.name
    FROM tweets t
    JOIN users u ON t.id_users = u.id_users
    ORDER BY t.created_at DESC, id_tweets
    LIMIT :limit OFFSET :offset;
    """
    engine = sqlalchemy.create_engine(psql_connection)
    connection = engine.connect()
    result = connection.execute(text(sqlcommand), {'limit': messages_per_page, 'offset': offset}).fetchall()
    connection.close()

    messages = [{'text': msg[0], 'created_at': msg[1], 'name': msg[2]} for msg in result]

    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)

    return render_template('root.html', logged_in=good_credentials, messages=messages, page=page)

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
            template = render_template('login.html', bad_credentials=False, logged_in=True)
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
