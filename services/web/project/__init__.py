import os
from sqlalchemy import text
from datetime import datetime

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    make_response,
    redirect,
    url_for
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # requests (plural) library for downloading;
    # now we need request singular 
    username = request.form.get('username')
    password = request.form.get('password')

    good_credentials = are_credentials_good(username, password)

    # the first time we've visited, no form submission
    if username is None:
        return render_template('login.html', bad_credentials=False)

    # they submitted a form; we're on the POST method
    else:
        if not good_credentials:
            return render_template('login.html', bad_credentials=True)
        else:
            # if we get here, then we're logged in
            # create a cookie that contains the username/password info

            template = render_template('login.html', bad_credentials=False, logged_in=True)
            
            response = make_response(template)
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
 
@app.route('/logout')
def logout():
    # Clear the cookies by setting them to expire immediately
    resp = make_response(redirect(url_for('login')))  # Redirect within the response
    resp.set_cookie('username', '', expires=0)       # Clear the username cookie
    resp.set_cookie('password', '', expires=0)       # Clear the password cookie
    return resp  # Return the modified response that redirects and clears cookies


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('create_account.html', error_message='Passwords do not match.')

        engine = sqlalchemy.create_engine(psql_connection)
        with engine.begin() as connection:  # Start a transaction
            # Check if the email is already in use
            sqlcommand = "SELECT count(*) FROM users WHERE name = :name"
            result = connection.execute(text(sqlcommand), {'name': name}).scalar()
            if result > 0:
                return render_template('create_account.html', error_message='Username already in use.')

            # Insert the new user if the email is not in use
            sqlcommand = "INSERT INTO users (name, password) VALUES (:name, :password)"
            connection.execute(text(sqlcommand), {'name': name, 'password': password})

        return redirect(url_for('login'))
    return render_template('create_account.html')



@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    pass


@app.route("/search", methods=["GET", "POST"])
def search():
    pass
